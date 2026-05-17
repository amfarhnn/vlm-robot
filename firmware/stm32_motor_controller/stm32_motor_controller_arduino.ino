/*
  Generic STM32 motor command receiver for the FYP robot.

  This template is intended for STM32duino-style development. The actual ROS
  Robot Control Board V3.0 may already provide firmware or a motor-control
  protocol. If so, keep the vendor firmware and map the RDK X5 command strings
  to the supported protocol.

  Update the pin definitions below according to the final motor driver wiring.
*/

const unsigned long BAUD_RATE = 115200;
const unsigned long COMMAND_TIMEOUT_MS = 1000;

const int BASE_SPEED = 90;
const int TURN_SPEED = 80;
const int SEARCH_SPEED = 65;

struct MotorPins {
  int pwm;
  int in1;
  int in2;
};

// Placeholder pins. Replace with pins used by the selected control board.
MotorPins frontLeft  = {PA0, PB0, PB1};
MotorPins frontRight = {PA1, PB10, PB11};
MotorPins rearLeft   = {PA2, PB12, PB13};
MotorPins rearRight  = {PA3, PB14, PB15};

unsigned long lastCommandMs = 0;

void setup() {
  Serial.begin(BAUD_RATE);
  setupMotor(frontLeft);
  setupMotor(frontRight);
  setupMotor(rearLeft);
  setupMotor(rearRight);
  stopAll();
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();
    executeCommand(command);
    lastCommandMs = millis();
  }

  if (millis() - lastCommandMs > COMMAND_TIMEOUT_MS) {
    stopAll();
  }
}

void setupMotor(MotorPins motor) {
  pinMode(motor.pwm, OUTPUT);
  pinMode(motor.in1, OUTPUT);
  pinMode(motor.in2, OUTPUT);
}

void executeCommand(String command) {
  if (command == "FWD") {
    moveForward(BASE_SPEED);
    Serial.println("ACK:FWD");
  } else if (command == "LEFT") {
    turnLeft(TURN_SPEED);
    Serial.println("ACK:LEFT");
  } else if (command == "RIGHT") {
    turnRight(TURN_SPEED);
    Serial.println("ACK:RIGHT");
  } else if (command == "SEARCH") {
    turnLeft(SEARCH_SPEED);
    Serial.println("ACK:SEARCH");
  } else {
    stopAll();
    Serial.println("ACK:STOP");
  }
}

void moveForward(int speedValue) {
  setMotor(frontLeft, speedValue);
  setMotor(frontRight, speedValue);
  setMotor(rearLeft, speedValue);
  setMotor(rearRight, speedValue);
}

void turnLeft(int speedValue) {
  setMotor(frontLeft, -speedValue);
  setMotor(rearLeft, -speedValue);
  setMotor(frontRight, speedValue);
  setMotor(rearRight, speedValue);
}

void turnRight(int speedValue) {
  setMotor(frontLeft, speedValue);
  setMotor(rearLeft, speedValue);
  setMotor(frontRight, -speedValue);
  setMotor(rearRight, -speedValue);
}

void stopAll() {
  setMotor(frontLeft, 0);
  setMotor(frontRight, 0);
  setMotor(rearLeft, 0);
  setMotor(rearRight, 0);
}

void setMotor(MotorPins motor, int speedValue) {
  speedValue = constrain(speedValue, -255, 255);

  if (speedValue > 0) {
    digitalWrite(motor.in1, HIGH);
    digitalWrite(motor.in2, LOW);
    analogWrite(motor.pwm, speedValue);
  } else if (speedValue < 0) {
    digitalWrite(motor.in1, LOW);
    digitalWrite(motor.in2, HIGH);
    analogWrite(motor.pwm, -speedValue);
  } else {
    digitalWrite(motor.in1, LOW);
    digitalWrite(motor.in2, LOW);
    analogWrite(motor.pwm, 0);
  }
}
