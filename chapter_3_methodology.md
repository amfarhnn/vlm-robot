# CHAPTER 3

# RESEARCH METHODOLOGY

## 3.1 Introduction

Chapter 2 identified a research gap in low-cost language-guided mobile robot navigation. Existing systems such as LM-Nav, VLMaps, HOV-SG, ViNT, NoMaD, VLMnav, NaVid, Uni-NaVid, and NaVILA show that language, vision, and action can be combined for robot navigation. However, many of these systems require expensive robot platforms, RGB-D cameras, LiDAR, mapping pipelines, server-level models, or complex navigation policies. This creates a practical gap for student-level implementation.

This chapter describes how the project addresses that gap through a low-cost indoor research prototype. The proposed system uses an RDK X5 development board with 8GB RAM as the onboard computing unit, a ROS Robot Control Board V3.0 with STM32F103RCT6 as the low-level motor controller, an ESP32 as the ultrasonic sensor controller, an unbranded 1080p USB webcam as the visual input sensor, four ultrasonic sensors as simple proximity sensors, four DC motors, a mobile robot chassis, and 18650 batteries. The robot is designed for controlled indoor testing in environments such as a corridor, room, laboratory, door area, signboard area, table area, and chair area.

The methodology is inspired by the modular structure of LM-Nav and the prompt-based action-selection idea of VLMnav. However, the methodology is adapted for this specific FYP prototype. The project does not attempt to build an industry-level autonomous navigation system. Instead, it studies whether structured prompt engineering can convert simple natural language instructions into useful navigation information, visually ground the target using a webcam image, and generate simple validated robot actions.

The intended action set is limited to:

- `move_forward`
- `turn_left`
- `turn_right`
- `stop`
- `search`

This restricted action set is suitable for the project because it allows the AI decision layer on the RDK X5 board to check obstacle readings from the ESP32 and communicate safely with the STM32-based motor controller. The main contribution of the methodology is therefore the design, implementation, and evaluation of a baseline prompt-engineered indoor navigation prototype that future researchers can improve.

## 3.2 Research Design and Project Workflow

The project follows an iterative prototyping methodology. This approach is suitable because the system contains hardware, software, AI processing, visual grounding, and motor-control components. Each component must be tested separately before the complete robot is evaluated in indoor navigation scenarios.

The methodology is organized around three main activities. First, the robot hardware and software platform are prepared. Second, prompt templates are designed to convert user instructions into structured navigation outputs. Third, the structured output, webcam image, and ESP32 ultrasonic readings are used to select a simple robot action, which is sent from the RDK X5 board to the STM32-based motor controller.

### 3.2.1 Methodology Alignment with Research Objectives

The methodology is aligned with the project objectives as shown in Table 3.1.

**Table 3.1: Methodology Alignment with Research Objectives**

| Research Objective | Method Used | Expected Output | Evaluation |
|---|---|---|---|
| Objective 1: To design a low-cost indoor mobile robot platform for prompt-based navigation | Build an RDK X5, STM32 motor control board, ESP32 ultrasonic sensing module, USB webcam, four-motor, chassis-based prototype | Functional robot platform for controlled indoor testing | Hardware setup test, webcam test, ESP32 ultrasonic sensor test, controller communication test, motor movement test |
| Objective 2: To develop prompt templates that extract structured navigation information from natural language | Design baseline, structured, relation-aware, and action-choice prompts | JSON-style output containing target, landmarks, spatial relation, action goal, suggested action, and uncertainty | Prompt output validity, landmark extraction accuracy, spatial relation extraction accuracy |
| Objective 3: To connect prompt output, webcam input, and obstacle sensing to simple robot actions | Use visual grounding or VLM-based action selection to choose from `move_forward`, `turn_left`, `turn_right`, `stop`, and `search`, then validate against ESP32 distance readings | Validated action command sent from RDK X5 to the STM32 motor control board | Visual grounding correctness, action selection accuracy, obstacle stop behavior, robot movement success, latency, failure analysis |

### 3.2.2 Overall Project Workflow

The overall project workflow begins with the preparation of the robot hardware and software environment. After the robot platform is functional, the prompt templates are developed and tested using sample instructions. The RDK X5 then captures a webcam image, processes the user instruction, performs visual grounding or action selection, receives ultrasonic distance readings from the ESP32 for basic safety, validates the output, and sends a simple command to the STM32-based motor control board. The robot control board drives the four DC motors according to the selected action.

The workflow is summarized in Figure 3.1.

**Figure 3.1: Proposed project workflow**

```text
Prepare Low-Cost Robot Hardware
        |
        v
Set Up RDK X5, Webcam, Python, and OpenCV
        |
        v
Set Up STM32 Motor Control and ESP32 Ultrasonic Sensing
        |
        v
Create Prompt Templates
        |
        v
Test Prompt Output with Sample Instructions
        |
        v
Capture Webcam Image
        |
        v
Visual Grounding or Action Selection
        |
        v
Is the output valid and confident?
    | yes
    v
Send Motor Command to STM32 Robot Control Board
        |
        v
Execute Robot Movement
        |
        v
Evaluate Scenario Result

If output is invalid or uncertain:
        -> stop robot, log failure, refine prompt or grounding method
```

### 3.2.3 Development Workflow

The development workflow is divided into stages so that hardware and software risks can be reduced before full integration.

**Table 3.2: Development Workflow**

| Stage | Activity | Expected Output |
|---|---|---|
| Stage 1 | Prepare robot hardware, including chassis, four DC motors, RDK X5, STM32 robot control board, ESP32, USB webcam, four ultrasonic sensors, and 18650 batteries | Assembled prototype robot |
| Stage 2 | Install and configure RDK X5 software, Python, OpenCV, webcam capture, and required AI libraries or API access | Working onboard computing environment |
| Stage 3 | Configure STM32 robot control board motor control and command handling | STM32 board can receive commands and control motors |
| Stage 4 | Configure ESP32 ultrasonic sensor reading and communication with RDK X5 | ESP32 can report obstacle or distance status |
| Stage 5 | Create prompt templates for landmark extraction, spatial relation extraction, and action selection | Tested prompt templates |
| Stage 6 | Test prompt output using sample instructions such as "Go to the door" and "Find the signboard" | Valid structured outputs |
| Stage 7 | Test webcam image capture and visual grounding with indoor landmarks | Grounding result or action recommendation |
| Stage 8 | Connect AI decision logic to ESP32 obstacle status and STM32 motor commands | End-to-end command flow from instruction to safe motor action |
| Stage 9 | Test indoor navigation scenarios in controlled areas | Scenario results and movement observations |
| Stage 10 | Collect, analyse, and report results, limitations, and future improvements | Final evaluation and discussion |

## 3.3 Proposed System Architecture

The proposed system architecture adapts the LM-Nav idea into a low-cost indoor robot system. LM-Nav separates language understanding, visual grounding, and navigation execution. In this project, these stages are implemented as user prompt processing, structured navigation output generation, webcam-based visual grounding or action selection, RDK X5 decision logic, ESP32 ultrasonic safety checking, STM32 motor command handling, and robot movement.

**Figure 3.2: Proposed system architecture**

```text
User Natural Language Prompt
        |
        v
RDK X5 Prompt Engineering Module
        |
        v
Structured Navigation Output
        |
        v
USB Webcam Image Capture
        |
        v
Visual Grounding or Action Selection
        |
        v
RDK X5 Decision and Validation Logic
        |
        v
Check ESP32 Ultrasonic Obstacle Status
        |
        v
Command to STM32 Robot Control Board
        |
        v
Four DC Motors and Chassis Movement
        |
        v
Robot Movement in Indoor Test Area
```

The architecture is intentionally modular. If the robot fails to reach the target, the failure can be traced to a specific component: prompt output, visual grounding, action selection, serial communication, motor control, or physical movement. This is important for an FYP because the project must be evaluated systematically rather than only judged by whether the robot moves.

### 3.3.1 Hardware Roles

The hardware components and their roles are shown in Table 3.3.

**Table 3.3: Proposed Hardware Components and Roles**

| Component | Role in the System | Reason for Selection |
|---|---|---|
| RDK X5 development board with 8GB RAM | Runs Python, receives the user instruction, captures webcam image, performs prompt processing or AI decision, receives obstacle status from ESP32, validates the selected action, and sends motor commands to the STM32 robot control board | Low-cost embedded AI/robotics computing board suitable for the high-level prototype pipeline |
| ROS Robot Control Board V3.0 with STM32F103RCT6 | Receives simple motor commands from the RDK X5 board and controls the DC motors | Suitable low-level controller for motor execution |
| ESP32 | Reads the four ultrasonic sensors and sends distance or obstacle status to the RDK X5 board | Suitable low-cost microcontroller for separating sensor timing from motor control |
| Unbranded 1080p USB webcam | Captures the indoor scene for visual grounding or action selection; supports USB plug-and-play, CMOS imaging, manual focus, auto white balance, and low-light correction | Low-cost RGB visual input suitable for indoor landmark testing |
| Four ultrasonic sensors | Provide simple distance or obstacle awareness around the robot through the ESP32 | Low-cost safety aid for controlled indoor testing |
| Four DC motors | Provide wheeled robot movement | Simple and low-cost movement mechanism for indoor prototype |
| Chassis | Holds the RDK X5 board, STM32 robot control board, ESP32, webcam, ultrasonic sensors, motors, and batteries | Affordable robot body for FYP development |
| Four 18650 batteries | Power the motors and electronics according to safe voltage requirements | Required for mobile operation |

The RDK X5 is responsible for high-level decision making, the STM32-based robot control board is responsible for low-level motor execution, and the ESP32 is responsible for ultrasonic sensor handling. This separation prevents the AI processing loop from directly controlling motor pins or ultrasonic timing and makes the system easier to test.

The webcam is used only as the visual input device for indoor scene observation. Although the selected webcam includes a microphone and supports video-compression features such as H.264/H.265, the main requirement for this project is its 1920 x 1080 RGB image capture through a plug-and-play USB connection. Audio input is not part of the baseline methodology unless voice-command input is added as future work.

## 3.4 System Requirements, Constraints, and Acceptance Criteria

The system requirements are defined according to the actual scope of the project. The prototype must be able to accept a simple navigation instruction, process the instruction into a structured format, use webcam input for grounding or action selection, and move the robot using validated commands.

**Table 3.4: Requirements and Acceptance Criteria**

| Requirement | Specification | Verification Method | Pass Criteria |
|---|---|---|---|
| Natural language input | The system accepts simple indoor navigation instructions | Instruction input test | Instruction is received without manual rewriting |
| Structured prompt output | The prompt produces a machine-readable response | JSON validation | Required fields are present and parseable |
| Landmark extraction | The system identifies target objects such as door, signboard, chair, table, or corridor | Comparison with expected labels | Correct target or landmark is extracted |
| Spatial relation extraction | The system identifies relations such as near, beside, after, or toward when present | Manual annotation comparison | Relevant relation is represented correctly |
| Webcam capture | RDK X5 captures the current indoor scene from the USB webcam | OpenCV camera test | Image frame is captured successfully |
| Visual grounding or action selection | The system connects the prompt output and image to an action decision | Scenario-based test | Selected action is relevant to the instruction and current view |
| Ultrasonic sensing | ESP32 reads four ultrasonic sensors and reports basic proximity status to the RDK X5 | ESP32 sensor reading and serial/status test | Distance values are received by the RDK X5 and can trigger stop behavior |
| Controller communication | RDK X5 receives ESP32 obstacle status and sends motor commands to the STM32 robot control board | Serial or command log inspection | ESP32 status and STM32 command strings are received correctly |
| Motor control | STM32 robot control board controls the motors according to command | Movement test | Robot performs the intended basic motion |
| Safety validation | Uncertain or invalid AI output is not executed directly | Failure-case test | Robot stops or requests refinement instead of moving unsafely |

The project has several constraints. The robot operates only in a controlled indoor environment. The webcam does not provide depth information. The project does not include full SLAM, LiDAR mapping, large VLA model deployment, or advanced learned navigation policies. These constraints are acceptable because the goal is to build and evaluate a baseline prompt-engineered prototype.

## 3.5 Data, Test Environment, and Experimental Materials

The project uses simple indoor navigation instructions and webcam images from controlled test areas. The instruction set is designed to represent common commands that a user may give to a small indoor mobile robot.

**Table 3.5: Instruction Categories and Indoor Landmarks**

| Category | Example Instruction | Target Landmark or Relation | Purpose |
|---|---|---|---|
| Single landmark | "Go to the door." | door | Test basic target extraction |
| Object search | "Find the signboard." | signboard | Test search behavior when target may not be centered |
| Landmark with relation | "Move toward the chair near the table." | chair near table | Test spatial relation extraction |
| Corridor navigation | "Move forward in the corridor." | corridor | Test action interpretation from scene context |
| Stop condition | "Stop at the door." | door and stop action | Test stopping behavior when target is detected |
| Ambiguous instruction | "Go there" or "Find it" | unclear target | Test uncertainty handling and safe stop behavior |

The indoor test environment will include simple visual landmarks such as a door, table, chair, signboard, corridor, wall, and room entrance. The environment should be controlled enough for safe movement but varied enough to test different prompt and grounding outcomes.

**Table 3.6: Experimental Materials**

| Material | Function |
|---|---|
| Navigation instruction list | Input for prompt engineering experiments |
| Expected landmark labels | Ground truth for extraction accuracy |
| Webcam images or live camera frames | Input for visual grounding and action selection |
| RDK X5 development board with 8GB RAM | Runs the high-level Python decision pipeline |
| ROS Robot Control Board V3.0 with STM32F103RCT6 | Runs low-level motor control for the four DC motors |
| ESP32 | Reads the four ultrasonic sensors and sends obstacle or distance status to the RDK X5 |
| Unbranded 1080p USB webcam | Provides RGB image input for grounding and action selection |
| Four ultrasonic sensors | Provide simple obstacle or proximity readings through the ESP32 |
| Four DC motors | Execute movement commands |
| Mobile robot chassis | Physical robot platform |
| Four 18650 batteries | Provide mobile power supply |
| Result log file | Stores instructions, prompt outputs, selected actions, movement results, latency, and failures |

**Table 3.7: Software, Model, and Platform Requirements**

| Item | Purpose | Planned Tool or Example |
|---|---|---|
| Operating environment | Run the robot software on RDK X5 | Linux-based RDK X5 environment |
| Programming language | Implement prompt processing, camera capture, decision logic, and logging | Python |
| Webcam processing | Capture and process RGB frames | OpenCV |
| Prompt processing model | Extract structured navigation information | GPT-style model, local LLM, or available API model |
| Visual grounding model | Match text target with webcam image or answer visual questions | CLIP, OpenCLIP, or VLM depending on available compute |
| Controller communication | Send obstacle status from ESP32 to RDK X5 and motor commands from RDK X5 to STM32 robot control board | Serial or supported robot control interface |
| ESP32 firmware | Read four ultrasonic sensors and report distance or obstacle status | Arduino IDE, PlatformIO, or ESP-IDF depending on development preference |
| STM32 robot control firmware | Receive motor commands and control the four DC motors | ROS Robot Control Board V3.0 firmware or compatible development workflow |
| Result storage | Record output and evaluation data | CSV, JSON, Markdown table, or spreadsheet |

## 3.6 Prompt Engineering Design

Prompt engineering is the central research element of the project. The prompt must convert a user instruction into a structured navigation representation that can be parsed by the RDK X5 board. The output should be simple enough for the robot to use, but detailed enough to preserve target, landmark, relation, action goal, and uncertainty information.

**Table 3.8: Prompt Templates for Evaluation**

| Prompt Type | Description | Expected Output |
|---|---|---|
| Baseline landmark prompt | Extracts only the main landmark from the instruction | Target landmark list |
| Structured navigation prompt | Requires fixed JSON fields for target, landmarks, relation, action goal, suggested action, and uncertainty | Parseable JSON-style navigation output |
| Relation-aware prompt | Emphasizes spatial phrases such as near, beside, toward, after, and at | Target plus spatial relation |
| Action-choice prompt | Restricts the model to choose from `move_forward`, `turn_left`, `turn_right`, `stop`, and `search` | Valid action label |
| Safety-aware prompt | Requires the model to return high uncertainty or stop when instruction is unclear | Safe output for ambiguous instructions |

The structured output format is shown below.

```json
{
  "target": "door",
  "landmarks": ["door"],
  "spatial_relation": null,
  "action_goal": "find and move toward the door",
  "suggested_action": "move_forward",
  "uncertainty": "low"
}
```

For a relation-based instruction, the expected output may be:

```json
{
  "target": "chair",
  "landmarks": ["chair", "table"],
  "spatial_relation": "chair near table",
  "action_goal": "move toward the chair that is near the table",
  "suggested_action": "search",
  "uncertainty": "medium"
}
```

**Table 3.9: Structured Output Fields**

| Field | Description | Example |
|---|---|---|
| `target` | Main object or place the robot should find or approach | `door` |
| `landmarks` | Important objects or places mentioned in the instruction | `["chair", "table"]` |
| `spatial_relation` | Relation between target and reference object, if present | `chair near table` |
| `action_goal` | Short natural-language goal for decision logic or logging | `find and move toward the door` |
| `suggested_action` | Proposed action from the fixed action set | `move_forward` |
| `uncertainty` | Confidence label used for safety validation | `low`, `medium`, or `high` |

The RDK X5 will validate this output before execution. If required fields are missing, if the action is outside the approved action set, if uncertainty is high, or if ESP32 ultrasonic readings indicate that the path is too close to an obstacle, the robot should stop and log the failure instead of moving.

## 3.7 Webcam-Based Visual Grounding and Action Selection

After the prompt output is generated, the system captures an image from the USB webcam. The image is used to decide whether the target appears in the current view and which action should be taken. The visual grounding stage may use CLIP, OpenCLIP, a VLM, or a simplified image-based method depending on available compute and implementation constraints.

For CLIP or OpenCLIP-style grounding, the text query may be the target alone, such as `door`, or a prompt-expanded query, such as `an indoor door in a corridor`. The basic score is:

```text
score(image, text) = cosine_similarity(E_image(image), E_text(text))
```

For VLM-style action selection, the model may be asked to choose the best action from the approved action set based on the instruction and current image. This follows the idea of VLMnav but is simplified for the FYP robot.

**Table 3.10: Visual Grounding and Action Selection Strategies**

| Strategy | Description | Suitability for This Prototype |
|---|---|---|
| Direct target grounding | Compare webcam image with the target word such as `door` or `chair` | Simple baseline for single-landmark instructions |
| Prompt-expanded grounding | Use a richer text query such as `a signboard on an indoor wall` | Useful when target needs more context |
| Relation-aware grounding | Include relation text such as `chair near table` | Useful for relation-based instructions, but may be harder with single RGB image |
| VLM action-choice prompt | Ask the model to choose from the fixed action set using image and instruction | Useful for direct decision making, but output must be validated |
| Rule-based fallback | If target is uncertain, use `search` or `stop` | Important for safety and baseline robustness |

The grounding result is not treated as perfect. The system will log cases where the target is not visible, the model selects the wrong action, or the robot needs to search.

## 3.8 Robot Action Set and Motor Command Mapping

The robot uses a small action set because the prototype is intended for controlled indoor testing. The RDK X5 selects a high-level action and sends the corresponding command string to the STM32-based robot control board. The robot control board then translates the command into motor signals.

**Table 3.11: Action Set and Motor Command Mapping**

| Action | Meaning | STM32 Robot Control Board Behavior |
|---|---|---|
| `move_forward` | Move the robot forward slowly | All four motors rotate forward at controlled speed |
| `turn_left` | Rotate or steer the robot left | Left-side motors slow or reverse, right-side motors move forward |
| `turn_right` | Rotate or steer the robot right | Right-side motors slow or reverse, left-side motors move forward |
| `stop` | Stop movement immediately | All motors stop |
| `search` | Rotate slowly or scan for target | Robot turns slowly while webcam continues checking scene |

This action set is intentionally limited. It does not include full path planning, obstacle avoidance, or continuous velocity control. The purpose is to test whether language and visual information can be converted into simple, safe movement commands.

## 3.9 Baseline Prototype and Future Improvement Scope

The baseline implementation focuses on simple indoor navigation using prompt engineering and webcam-based grounding. More advanced methods from the literature are treated as future improvements.

**Table 3.12: Baseline and Future Improvement Methods**

| Method | Role in This Project | Decision |
|---|---|---|
| LM-Nav-style modular pipeline | Provides the conceptual structure of language understanding, visual grounding, and execution | Used as the main baseline inspiration |
| VLMnav-style action-choice prompt | Supports selecting from a fixed action set | Used as a prompt/action-selection reference |
| CLIP or OpenCLIP grounding | Allows text target and image comparison | Used if compute and implementation are practical |
| RGB-D mapping | Improves depth and spatial understanding | Future work |
| LiDAR-based obstacle detection | Improves safety and mapping | Future work due to cost and complexity |
| VLMaps or HOV-SG-style spatial memory | Supports map and scene-graph reasoning | Future work |
| ViNT or NoMaD navigation policy | Replaces simple action control with stronger navigation execution | Future work |
| Large VLM or VLA model pipeline | Improves reasoning but requires more compute | Future work or optional remote testing |

This table clarifies the scope of the FYP. The project is not evaluated as a complete industrial navigation stack. It is evaluated as a baseline research prototype that can support later improvements.

## 3.10 Mechanical Design and Physical Integration

The mobile robot chassis will be designed as a purpose-built low-cost platform for the project. The design is prepared in Autodesk Fusion 360 so that the RDK X5 board, STM32 robot control board, ESP32, webcam, ultrasonic sensors, battery holder, and four DC motors can be mounted in a controlled and repeatable layout. The 3D model is not treated as the main research contribution, but it is important because the sensor placement and component arrangement affect the reliability of the indoor navigation experiment.

The proposed chassis should provide mounting space for the webcam at the front of the robot, four ultrasonic sensors around the robot body, and accessible mounting positions for the controller boards. The battery holder should be placed low on the chassis to improve stability. The design should also allow the wiring to be routed safely so that cables do not touch the wheels or motors.

**Figure 3.3: Placeholder for proposed Fusion 360 3D robot model**

```text
Insert Fusion 360 3D model image here.

Suggested image content:
- Isometric view of the complete 3D-printed chassis
- Mounting position for RDK X5
- Mounting position for STM32 robot control board
- Mounting position for ESP32
- Webcam position
- Four ultrasonic sensor positions
- Four DC motor and wheel positions
- Battery holder position
```

### 3.10.1 Suggested Circuit Architecture

The circuit architecture is divided into three layers: computing, sensing, and motion. The RDK X5 performs high-level prompt processing and decision logic. The ESP32 handles the timing-sensitive ultrasonic sensor readings. The STM32-based robot control board receives validated motor commands and controls the motors. This separation is suitable for an FYP prototype because each layer can be tested independently before full integration.

**Figure 3.4: Suggested circuit architecture**

```text
4x 18650 Battery Pack
        |
        v
Main Power Switch and Fuse
        |
        +--> Motor Power Rail
        |       |
        |       v
        |   STM32 Robot Control Board or Motor Driver
        |       |
        |       +--> Front Left DC Motor
        |       +--> Front Right DC Motor
        |       +--> Rear Left DC Motor
        |       +--> Rear Right DC Motor
        |
        +--> Regulated 5 V Supply
                |
                +--> RDK X5 Development Board
                |       |
                |       +--> USB Webcam
                |       +--> USB or UART link to ESP32
                |       +--> USB or UART link to STM32 Robot Control Board
                |
                +--> ESP32
                        |
                        +--> Front Ultrasonic Sensor
                        +--> Left Ultrasonic Sensor
                        +--> Right Ultrasonic Sensor
                        +--> Rear Ultrasonic Sensor

All grounds are connected to a common ground reference.
```

The final circuit diagram should show the battery connection, power switch, regulator, RDK X5, ESP32, STM32 robot control board, ultrasonic sensors, motor driver outputs, and motors. If the ultrasonic sensors are powered at 5 V, the echo signals should be reduced to 3.3 V before entering ESP32 input pins. This can be done using a voltage divider or logic-level shifter. The exact pin numbers should be confirmed after the physical boards and connectors are finalized.

**Figure 3.5: Placeholder for final circuit diagram**

```text
Insert final circuit diagram picture here.

Suggested circuit diagram content:
- Battery pack, switch, fuse, and regulator
- RDK X5 power input and USB webcam connection
- RDK X5 serial connection to ESP32
- RDK X5 serial connection to STM32 robot control board
- ESP32 trigger and echo pins to four ultrasonic sensors
- STM32 robot control board or motor driver output to four DC motors
- Common ground connection
- Emergency stop or manual power switch
```

## 3.11 Company, Software, and Tool Involvement

The project does not involve industrial sponsorship. However, several hardware and software vendors, chip manufacturers, and open-source tools are used in the prototype. Table 3.13 identifies the companies or organizations related to the selected components and software tools. For final submission, the exact supplier name should be checked against the purchase receipt or product label, especially for unbranded or third-party robot-control boards.

**Table 3.13: Company, Component, and Software Involvement**

| Component or Tool | Company or Organization | Involvement in This Project | Notes for Final Report |
|---|---|---|---|
| RDK X5 development board | D-Robotics | Main onboard computing board for Python, webcam capture, and AI decision logic | Use the exact board documentation or supplier listing when confirming specifications |
| STM32F103RCT6 microcontroller | STMicroelectronics | Microcontroller used on the ROS Robot Control Board V3.0 | Used indirectly through the robot control board firmware |
| ROS Robot Control Board V3.0 | Yahboom listing or exact supplier to be confirmed from purchase source | Low-level motor command execution and motor-driver interface | Record exact supplier, product store, and board revision after purchase confirmation |
| ESP32 microcontroller | Espressif Systems | Ultrasonic sensor controller and serial status transmitter | Used to separate sensor timing from high-level AI processing |
| USB webcam | Unbranded manufacturer | RGB visual input for indoor scene capture | Webcam is treated as a low-cost plug-and-play RGB camera |
| Autodesk Fusion 360 | Autodesk | 3D modelling software for the robot chassis design | Used for mechanical design documentation |
| Python | Python Software Foundation | Main programming language for RDK X5 control logic | Used for prompt parsing, decision logic, camera capture, and logging |
| OpenCV | OpenCV project | Webcam frame capture and basic image processing | Used before advanced CLIP or VLM grounding is added |
| Arduino IDE, PlatformIO, or ESP-IDF | Arduino, PlatformIO Labs, or Espressif Systems | Firmware development for ESP32 and possible STM32 template testing | Tool choice depends on the final firmware workflow |
| diagrams.net or draw.io | JGraph or diagrams.net project | Diagram preparation for system architecture and circuit documentation | Used for report figures and flowcharts |

## 3.12 Software Implementation and Coding

The baseline coding is divided according to the hardware roles. The RDK X5 runs the main Python control program. The ESP32 runs firmware that reads four ultrasonic sensors and sends JSON status messages. The STM32 robot control board receives simple motor commands. If the selected STM32 board already provides vendor firmware, the vendor firmware should be used and the RDK X5 command strings should be mapped to the supported command protocol. If custom firmware is required, the provided STM32 template can be adapted after confirming the board pinout.

The full baseline source code is provided in the project repository so that the methodology is supported by an implementable software structure rather than only a conceptual flowchart.

**Table 3.14: Source Code Modules for Baseline Implementation**

| File | Hardware Target | Purpose | Status |
|---|---|---|---|
| `src/rdk_x5/robot_navigation_controller.py` | RDK X5 | Runs prompt parsing, webcam capture, ESP32 status reading, action validation, STM32 command sending, and logging | Baseline implementation provided |
| `src/rdk_x5/config.example.json` | RDK X5 | Stores webcam index, serial ports, baud rate, safety threshold, and log paths | Example configuration provided |
| `src/rdk_x5/requirements.txt` | RDK X5 | Lists Python packages for webcam capture and serial communication | Baseline dependency list provided |
| `firmware/esp32_ultrasonic_hub/esp32_ultrasonic_hub.ino` | ESP32 | Reads four ultrasonic sensors and outputs JSON distance and obstacle status | Baseline firmware provided |
| `firmware/stm32_motor_controller/stm32_motor_controller_arduino.ino` | STM32 robot control board or compatible STM32duino setup | Receives `FWD`, `LEFT`, `RIGHT`, `STOP`, and `SEARCH` commands and converts them to motor outputs | Pin-configurable template provided |
| `docs/circuit_wiring_guide.md` | Documentation | Provides text-form wiring guidance for the proposed circuit architecture | Draft wiring guide provided |

The RDK X5 controller follows the control logic shown below:

```text
Receive user instruction
Generate structured prompt output
Capture webcam frame
Read ESP32 ultrasonic distance status
Select proposed action from fixed action set
If output is invalid, uncertainty is high, or obstacle is detected:
    execute stop
Else:
    send validated command to STM32 robot control board
Log instruction, structured output, sensor status, final action, and latency
```

This coding structure is influenced by LM-Nav and VLMnav but simplified for the proposed hardware. LM-Nav motivates the separation between language understanding, visual grounding, and execution. VLMnav motivates the use of action-choice prompting from a fixed action set. CLIP or OpenCLIP can be added later to replace the current baseline grounding function. VLMaps, HOV-SG, ViNT, NoMaD, NaVid, Uni-NaVid, and NaVILA are not implemented in the first prototype because they require additional sensors, mapping, model deployment, or compute resources beyond the initial FYP scope.

## 3.13 Equations and Decision Rules

The project uses simple equations and decision rules to evaluate the prototype. The equations are not intended to represent a complete navigation theory; they provide measurable criteria for prompt quality, visual grounding, action selection, ultrasonic safety checking, and response time.

**Table 3.15: Main Equations and Decision Rules**

| Equation or Rule | Description | Use in Evaluation |
|---|---|---|
| `d_cm = t_echo_us / 58` | Approximate ultrasonic distance where `t_echo_us` is the echo pulse duration in microseconds | Converts ESP32 ultrasonic timing into distance in centimetres |
| `S(I,T) = cosine(E_image(I), E_text(T))` | CLIP or OpenCLIP similarity between image embedding and text embedding | Optional visual grounding score when CLIP-style grounding is used |
| `Prompt Validity = N_valid / N_total * 100 percent` | Percentage of prompt outputs that contain required fields and valid JSON structure | Measures structured output reliability |
| `Accuracy = N_correct / N_total * 100 percent` | General accuracy formula for landmark extraction, relation extraction, grounding, or action selection | Allows consistent metric reporting |
| `T_total = T_prompt + T_capture + T_grounding + T_sensor + T_serial` | Total response time from instruction input to command output | Measures system latency |
| `a_exec = stop if invalid output, high uncertainty, unsafe distance, or invalid action; otherwise a_selected` | Safety validation rule before motor command execution | Prevents uncertain AI output from becoming unsafe movement |
| `Movement Success Rate = N_success / N_scenarios * 100 percent` | Percentage of indoor scenarios where the robot performs the intended simple action | Measures physical robot performance |

For ultrasonic sensing, an obstacle is considered present when the smallest valid distance from the ESP32 is lower than the selected safety threshold. In the baseline configuration, the threshold is set to 25 cm, but this value can be adjusted during testing depending on robot speed, braking distance, and sensor reliability.

## 3.14 Implementation Procedure

The implementation procedure follows ten stages. Each stage has a verification method so that the project can be developed and tested systematically.

**Table 3.16: Implementation Procedure**

| Stage | Activity | Verification | Expected Result |
|---|---|---|---|
| Stage 1 | Prepare robot hardware, including chassis, four DC motors, RDK X5, ROS Robot Control Board V3.0 with STM32F103RCT6, ESP32, webcam, four ultrasonic sensors, and 18650 batteries | Physical inspection and wiring check | Robot hardware is assembled safely |
| Stage 2 | Set up RDK X5, Python environment, OpenCV, webcam access, and required model or API access | Run camera capture and Python test scripts | RDK X5 can capture images and run the decision pipeline |
| Stage 3 | Set up STM32 robot control board firmware, motor control, and command handling | Send test commands from computer or RDK X5 | Robot control board receives commands and drives motors correctly |
| Stage 4 | Set up ESP32 firmware, ultrasonic sensor reading, and communication with the RDK X5 | Compare serial/status output with measured distances | ESP32 reports usable distance or obstacle status |
| Stage 5 | Create prompt templates for baseline, structured, relation-aware, action-choice, and safety-aware outputs | Prompt tests using sample instructions | Prompt returns parseable structured output |
| Stage 6 | Test prompt output using sample instructions | Compare output with expected labels | Landmark, relation, action, and uncertainty fields are correct |
| Stage 7 | Test webcam image capture and visual grounding | Compare grounding output with known target image or scene | Target or action decision is reasonable |
| Stage 8 | Connect AI decision to ESP32 obstacle status and STM32 motor action | Send selected command to STM32 robot control board after validation | Robot moves only when the action is valid and the path is safe enough |
| Stage 9 | Test indoor navigation scenarios with door, signboard, chair, table, and corridor | Scenario checklist and video/log review | Robot performs basic movement toward or search behavior |
| Stage 10 | Collect and analyse results | Metric calculation and failure-case analysis | Final performance, limitations, and future work are documented |

## 3.15 Testing and Validation Plan

Testing is divided into module testing, integration testing, and scenario testing. Module testing checks the prompt, webcam, grounding, ESP32 ultrasonic sensing, controller communication, and motor control separately. Integration testing checks whether the system can process an instruction, capture an image, select an action, check ESP32 proximity readings, and send a command to the STM32 robot control board. Scenario testing evaluates the robot in controlled indoor environments.

**Table 3.17: Testing and Validation Matrix**

| Test Stage | Test Setup | Metric | Pass Criteria |
|---|---|---|---|
| Prompt format test | Input instructions only | Prompt output validity | Output follows required JSON fields |
| Landmark extraction test | Instructions with known targets | Landmark extraction accuracy | Correct target and landmark list are extracted |
| Spatial relation test | Instructions with relation labels | Spatial relation extraction accuracy | Relation such as `chair near table` is represented correctly |
| Webcam capture test | USB webcam connected to RDK X5 | Frame capture success | Image frame is captured reliably |
| Visual grounding test | Webcam image and target text | Grounding correctness | Correct target is identified or uncertainty is reported |
| Action selection test | Instruction and current webcam view | Action selection accuracy | Selected action matches expected behavior |
| Ultrasonic sensor test | Four ultrasonic sensors connected to ESP32 | Distance reading availability | ESP32 readings are available for simple safety checks |
| Controller communication test | ESP32 reports status to RDK X5 and RDK X5 sends command to STM32 robot control board | Status and command delivery | RDK X5 receives valid obstacle status and robot control board receives valid command string |
| Motor movement test | STM32 robot control board controls motors | Movement correctness | Robot moves forward, turns, searches, or stops correctly |
| Full scenario test | Indoor target such as door, signboard, chair, table, or corridor | Robot movement success | Robot performs the intended simple navigation behavior |
| Safety test | Ambiguous or invalid instruction | Safe failure behavior | Robot stops or refuses uncertain action |
| Latency test | Full instruction-to-command pipeline | Response time | Command is produced within acceptable delay for prototype testing |

## 3.16 Evaluation Metrics

The evaluation focuses on both AI output quality and robot behavior. This is important because a prompt may produce a correct text output while the robot still fails to move correctly, or the robot may move correctly even when visual grounding is weak.

**Table 3.18: Evaluation Metrics**

| Metric | Description |
|---|---|
| Prompt output validity | Percentage of outputs that contain all required structured fields |
| Landmark extraction accuracy | Percentage of instructions where the correct target or landmarks are extracted |
| Spatial relation extraction accuracy | Percentage of relation-based instructions where the relation is correctly represented |
| Visual grounding correctness | Percentage of cases where the target is correctly matched or identified in the webcam view |
| Action selection accuracy | Percentage of cases where the selected action matches the expected action |
| Robot movement success | Percentage of scenarios where the robot performs the intended basic movement |
| Safe stop rate | Percentage of uncertain or invalid cases where the robot stops instead of executing unsafe output |
| Latency or response time | Time from user instruction to selected command |
| Failure-case count | Number and type of failures such as wrong target, invalid JSON, weak grounding, wrong turn, motor error, or unsafe suggestion |

Qualitative analysis will also be conducted. Failure cases will be grouped into prompt errors, grounding errors, action-selection errors, serial communication errors, motor-control errors, and environmental limitations. This helps identify whether future work should improve prompts, visual grounding, hardware, or navigation control.

## 3.17 Safety, Ethics, and Practical Considerations

Safety is important even though the robot is a low-cost indoor prototype. The robot should move at low speed during testing. All tests should be conducted in a controlled indoor area with sufficient space. A manual stop or emergency stop method should be available during movement tests. The four ultrasonic sensors connected to the ESP32 should be used as a simple proximity safety layer, but testing must still be supervised manually because ultrasonic sensors do not provide complete obstacle understanding.

The system should not execute uncertain AI output directly. If the structured output is invalid, if the selected action is not in the approved action set, or if the uncertainty is high, the robot should stop and log the case. This prevents a hallucinated or ambiguous model response from becoming an unsafe motor command.

Privacy must also be considered when using a webcam. Testing should avoid capturing identifiable people unless permission is obtained. Images and logs should be used only for project evaluation.

## 3.18 Limitations and Future Work

The proposed prototype has clear limitations. It uses a USB webcam, so it does not directly estimate dense depth or build a 3D map. The ESP32-based ultrasonic sensing module provides only simple distance cues and is not equivalent to LiDAR or RGB-D mapping. The system uses a simple action set, so it cannot perform full path planning. It does not include LiDAR, RGB-D SLAM, 3D scene graph mapping, or a learned navigation policy. It also depends on the reliability of prompt output and visual grounding.

These limitations are acceptable because the project is designed as a baseline research prototype. Future work can improve the system by adding an RGB-D camera, LiDAR, stronger obstacle sensing, map building, VLMaps-style visual-language maps, HOV-SG-style scene graphs, ViNT or NoMaD navigation policies, or more advanced VLM/VLA models. The baseline prototype provides a practical platform for these improvements by establishing the first connection between natural language prompts, webcam-based grounding, ESP32-based ultrasonic safety checking, and STM32-controlled robot movement.

## 3.19 Summary

This chapter presented the methodology for the proposed low-cost indoor mobile robot navigation prototype. The system is inspired by LM-Nav and VLMnav but is adapted for an FYP-scale implementation using an RDK X5 development board with 8GB RAM, ROS Robot Control Board V3.0 with STM32F103RCT6 for motor control, ESP32 for ultrasonic sensing, unbranded USB webcam, four ultrasonic sensors, four DC motors, chassis, and 18650 batteries.

The methodology defines the system architecture, hardware roles, mechanical and circuit integration plan, software tools, source-code structure, prompt engineering design, structured output format, visual grounding and action-selection process, action set, implementation stages, testing plan, evaluation metrics, safety considerations, and future work. The project is positioned as a baseline prototype that investigates how structured prompt engineering can support simple indoor robot navigation, while leaving advanced mapping, sensing, and navigation policies for future researchers.
