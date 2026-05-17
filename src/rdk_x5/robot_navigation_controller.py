#!/usr/bin/env python3
"""
Baseline RDK X5 controller for the FYP project:
Prompt Engineering for Mobile Robot Navigation.

The script is intentionally conservative. It demonstrates the complete
software flow from natural language instruction to validated robot command:

1. Parse a natural language instruction into structured navigation fields.
2. Capture a webcam frame for visual grounding or future VLM use.
3. Read ESP32 ultrasonic status.
4. Validate the selected action.
5. Send a simple motor command to the STM32 robot control board.

The prompt parser and grounding stage are baseline implementations. They can
be replaced later with an LLM, CLIP/OpenCLIP, or VLM action-choice model.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import cv2
except ImportError:  # pragma: no cover - handled at runtime on the robot
    cv2 = None

try:
    import serial
except ImportError:  # pragma: no cover - handled at runtime on the robot
    serial = None


APPROVED_ACTIONS = {"move_forward", "turn_left", "turn_right", "stop", "search"}
KNOWN_LANDMARKS = [
    "door",
    "signboard",
    "chair",
    "table",
    "corridor",
    "room",
    "lab",
    "laboratory",
    "wall",
    "entrance",
]

ACTION_TO_STM32_COMMAND = {
    "move_forward": "FWD",
    "turn_left": "LEFT",
    "turn_right": "RIGHT",
    "stop": "STOP",
    "search": "SEARCH",
}


@dataclass
class NavigationOutput:
    target: str | None
    landmarks: list[str]
    spatial_relation: str | None
    action_goal: str
    suggested_action: str
    uncertainty: str


@dataclass
class SensorStatus:
    front_cm: float | None = None
    left_cm: float | None = None
    right_cm: float | None = None
    rear_cm: float | None = None
    obstacle: bool = False
    min_cm: float | None = None
    source: str = "not_available"


@dataclass
class DecisionRecord:
    timestamp: float
    instruction: str
    navigation: NavigationOutput
    sensor_status: SensorStatus
    grounding_status: str
    final_action: str
    stm32_command: str
    reason: str
    latency_ms: float


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_landmarks(instruction: str) -> list[str]:
    text = normalize_text(instruction)
    found: list[str] = []
    for landmark in KNOWN_LANDMARKS:
        if re.search(rf"\b{re.escape(landmark)}\b", text):
            found.append(landmark)
    return found


def extract_relation(instruction: str, landmarks: list[str]) -> str | None:
    text = normalize_text(instruction)
    relation_words = [
        "near",
        "beside",
        "next to",
        "in front of",
        "behind",
        "after",
        "before",
        "toward",
        "at",
    ]
    for relation in relation_words:
        if relation in text and len(landmarks) >= 2:
            return f"{landmarks[0]} {relation} {landmarks[1]}"
        if relation in text and len(landmarks) == 1:
            return f"{relation} {landmarks[0]}"
    return None


def choose_target(instruction: str, landmarks: list[str]) -> str | None:
    if not landmarks:
        return None
    text = normalize_text(instruction)
    for keyword in ["door", "signboard", "chair", "table", "corridor"]:
        if keyword in landmarks and re.search(rf"\b{keyword}\b", text):
            return keyword
    return landmarks[0]


def baseline_prompt_engineering(instruction: str) -> NavigationOutput:
    text = normalize_text(instruction)
    landmarks = extract_landmarks(text)
    target = choose_target(text, landmarks)
    relation = extract_relation(text, landmarks)

    if "stop" in text:
        action = "stop"
    elif not target:
        action = "stop"
    elif "find" in text or relation is not None:
        action = "search"
    elif "left" in text:
        action = "turn_left"
    elif "right" in text:
        action = "turn_right"
    else:
        action = "move_forward"

    if not target:
        uncertainty = "high"
        goal = "instruction is unclear; stop for safety"
    elif relation is not None:
        uncertainty = "medium"
        goal = f"find and move toward {relation}"
    else:
        uncertainty = "low"
        goal = f"find and move toward the {target}"

    return NavigationOutput(
        target=target,
        landmarks=landmarks,
        spatial_relation=relation,
        action_goal=goal,
        suggested_action=action,
        uncertainty=uncertainty,
    )


class JsonSerialReader:
    def __init__(self, port: str | None, baudrate: int, timeout: float = 0.1) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.device = None

    def __enter__(self) -> "JsonSerialReader":
        if not self.port or serial is None:
            return self
        try:
            self.device = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2.0)
        except Exception as exc:  # pragma: no cover - depends on hardware
            logging.warning("Could not open ESP32 serial port %s: %s", self.port, exc)
            self.device = None
        return self

    def __exit__(self, *_: object) -> None:
        if self.device:
            self.device.close()

    def read_status(self, safe_distance_cm: float) -> SensorStatus:
        if not self.device:
            return SensorStatus(source="dry_run_or_missing_serial")

        latest: dict[str, Any] | None = None
        end_time = time.time() + 0.35
        while time.time() < end_time:
            raw = self.device.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue
            try:
                latest = json.loads(raw)
            except json.JSONDecodeError:
                logging.debug("Ignoring non-JSON ESP32 line: %s", raw)

        if latest is None:
            return SensorStatus(source="esp32_no_recent_json")

        distances = [
            latest.get("front_cm"),
            latest.get("left_cm"),
            latest.get("right_cm"),
            latest.get("rear_cm"),
        ]
        numeric = [float(value) for value in distances if isinstance(value, (int, float))]
        min_cm = min(numeric) if numeric else None
        obstacle = bool(latest.get("obstacle", False))
        if min_cm is not None and min_cm < safe_distance_cm:
            obstacle = True

        return SensorStatus(
            front_cm=as_float(latest.get("front_cm")),
            left_cm=as_float(latest.get("left_cm")),
            right_cm=as_float(latest.get("right_cm")),
            rear_cm=as_float(latest.get("rear_cm")),
            obstacle=obstacle,
            min_cm=min_cm,
            source="esp32",
        )


class CommandSerialWriter:
    def __init__(self, port: str | None, baudrate: int, dry_run: bool) -> None:
        self.port = port
        self.baudrate = baudrate
        self.dry_run = dry_run
        self.device = None

    def __enter__(self) -> "CommandSerialWriter":
        if self.dry_run or not self.port or serial is None:
            return self
        try:
            self.device = serial.Serial(self.port, self.baudrate, timeout=0.1)
            time.sleep(2.0)
        except Exception as exc:  # pragma: no cover - depends on hardware
            logging.warning("Could not open STM32 serial port %s: %s", self.port, exc)
            self.device = None
        return self

    def __exit__(self, *_: object) -> None:
        if self.device:
            self.device.close()

    def send(self, command: str) -> None:
        line = f"{command}\n"
        if self.device:
            self.device.write(line.encode("utf-8"))
            self.device.flush()
        else:
            logging.info("DRY RUN STM32 command: %s", command)


def as_float(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def capture_webcam_frame(webcam_index: int, output_dir: Path) -> Path | None:
    if cv2 is None:
        logging.warning("OpenCV is not installed; skipping webcam capture.")
        return None

    output_dir.mkdir(parents=True, exist_ok=True)
    camera = cv2.VideoCapture(webcam_index)
    if not camera.isOpened():
        logging.warning("Could not open webcam index %s.", webcam_index)
        return None

    ok, frame = camera.read()
    camera.release()
    if not ok:
        logging.warning("Webcam opened but no frame was captured.")
        return None

    frame_path = output_dir / f"frame_{int(time.time() * 1000)}.jpg"
    cv2.imwrite(str(frame_path), frame)
    return frame_path


def baseline_grounding_decision(
    navigation: NavigationOutput,
    manual_grounding: str,
) -> tuple[str, str]:
    """
    Returns a possibly updated action and a grounding status.

    This baseline does not claim object detection. During early hardware tests,
    use --manual-grounding visible/not_visible/unknown. Later, this function can
    be replaced by CLIP/OpenCLIP scoring or VLM action-choice prompting.
    """
    if manual_grounding == "visible" and navigation.suggested_action == "search":
        return "move_forward", "manual_visible"
    if manual_grounding == "not_visible" and navigation.suggested_action == "move_forward":
        return "search", "manual_not_visible"
    return navigation.suggested_action, manual_grounding


def validate_action(
    navigation: NavigationOutput,
    proposed_action: str,
    sensor_status: SensorStatus,
) -> tuple[str, str]:
    if proposed_action not in APPROVED_ACTIONS:
        return "stop", "action_not_in_approved_set"
    if navigation.uncertainty == "high":
        return "stop", "high_prompt_uncertainty"
    if sensor_status.obstacle and proposed_action in {"move_forward", "turn_left", "turn_right", "search"}:
        return "stop", "obstacle_detected_by_esp32"
    return proposed_action, "validated"


def append_log(path: Path, record: DecisionRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(record)
    path.open("a", encoding="utf-8").write(json.dumps(data) + "\n")


def run_once(
    instruction: str,
    config: dict[str, Any],
    esp32_reader: JsonSerialReader,
    stm32_writer: CommandSerialWriter,
    manual_grounding: str,
) -> DecisionRecord:
    start = time.perf_counter()
    navigation = baseline_prompt_engineering(instruction)
    capture_webcam_frame(
        int(config.get("webcam_index", 0)),
        Path(config.get("camera_output_dir", "logs/frames")),
    )
    sensor_status = esp32_reader.read_status(float(config.get("safe_distance_cm", 25.0)))
    proposed_action, grounding_status = baseline_grounding_decision(navigation, manual_grounding)
    final_action, reason = validate_action(navigation, proposed_action, sensor_status)
    stm32_command = ACTION_TO_STM32_COMMAND[final_action]
    stm32_writer.send(stm32_command)
    latency_ms = (time.perf_counter() - start) * 1000.0

    record = DecisionRecord(
        timestamp=time.time(),
        instruction=instruction,
        navigation=navigation,
        sensor_status=sensor_status,
        grounding_status=grounding_status,
        final_action=final_action,
        stm32_command=stm32_command,
        reason=reason,
        latency_ms=latency_ms,
    )
    append_log(Path(config.get("log_path", "logs/run_log.jsonl")), record)
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Baseline RDK X5 robot navigation controller.")
    parser.add_argument("--config", default="config.example.json", help="Path to JSON config file.")
    parser.add_argument("--instruction", help="Single natural language navigation instruction.")
    parser.add_argument("--interactive", action="store_true", help="Read instructions from the terminal.")
    parser.add_argument(
        "--manual-grounding",
        choices=["visible", "not_visible", "unknown"],
        default="unknown",
        help="Temporary grounding label before CLIP/VLM integration.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not open STM32 serial output.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    config = load_config(Path(args.config))
    if args.dry_run:
        config["dry_run"] = True

    baudrate = int(config.get("baudrate", 115200))
    esp32_port = None if bool(config.get("dry_run", True)) else config.get("esp32_port")
    with JsonSerialReader(esp32_port, baudrate) as esp32_reader:
        with CommandSerialWriter(config.get("stm32_port"), baudrate, bool(config.get("dry_run", True))) as stm32_writer:
            if args.instruction:
                record = run_once(args.instruction, config, esp32_reader, stm32_writer, args.manual_grounding)
                print(json.dumps(asdict(record), indent=2))
                return

            if args.interactive:
                print("Enter instruction, or 'q' to quit.")
                while True:
                    instruction = input("> ").strip()
                    if instruction.lower() in {"q", "quit", "exit"}:
                        stm32_writer.send("STOP")
                        break
                    if instruction:
                        record = run_once(instruction, config, esp32_reader, stm32_writer, args.manual_grounding)
                        print(json.dumps(asdict(record), indent=2))
                return

    raise SystemExit("Provide --instruction or --interactive.")


if __name__ == "__main__":
    main()
