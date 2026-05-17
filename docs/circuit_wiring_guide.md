# Suggested Circuit Wiring Guide

This guide describes the proposed wiring architecture in text form. Final pin
numbers must be checked against the exact ROS Robot Control Board V3.0,
ESP32 board, motor driver, battery holder, and ultrasonic sensor modules used
in the physical prototype.

## High-Level Connection

```text
User prompt
  -> RDK X5 high-level Python controller
  -> ESP32 ultrasonic status check
  -> STM32 robot control board motor command
  -> motor driver outputs
  -> four DC motors
```

## Suggested Circuit Diagram in Text Form

```text
[4x 18650 Battery Pack]
        |
        v
[Main Power Switch / Fuse]
        |
        +--> [Motor Power Rail] --> [STM32 Robot Control Board / Motor Driver]
        |                                  |--> Front Left DC Motor
        |                                  |--> Front Right DC Motor
        |                                  |--> Rear Left DC Motor
        |                                  |--> Rear Right DC Motor
        |
        +--> [Regulated 5 V Supply] --> [RDK X5 Development Board]
        |                                  |--> USB Webcam
        |                                  |--> USB/UART to ESP32
        |                                  |--> USB/UART to STM32 board
        |
        +--> [Regulated 5 V or 3.3 V Supply] --> [ESP32]
                                               |--> Ultrasonic Sensor Front
                                               |--> Ultrasonic Sensor Left
                                               |--> Ultrasonic Sensor Right
                                               |--> Ultrasonic Sensor Rear

All controller grounds must be connected to a common ground reference.
```

## ESP32 to Ultrasonic Sensors

Each ultrasonic sensor has four typical pins:

- VCC: connect to the sensor supply voltage specified by the sensor module.
- GND: connect to common ground.
- TRIG: connect to an ESP32 output GPIO.
- ECHO: connect to an ESP32 input GPIO through level shifting if the echo
  voltage is higher than 3.3 V.

Suggested logical placement:

- Front sensor: detects obstacle in front of the robot.
- Left sensor: checks left-side clearance.
- Right sensor: checks right-side clearance.
- Rear sensor: optional reverse safety or rear proximity checking.

## RDK X5 to Controllers

- RDK X5 to ESP32: USB serial or UART serial for JSON distance/status messages.
- RDK X5 to STM32 board: USB serial or UART serial for motor commands such as
  FWD, LEFT, RIGHT, STOP, and SEARCH.
- USB webcam to RDK X5: direct USB connection.

## Safety Notes

- Do not power the RDK X5 directly from an unregulated battery pack.
- Use a regulator or power module that matches the RDK X5 input requirement.
- Use a main switch and preferably a fuse on the battery supply.
- Use common ground between the RDK X5, ESP32, STM32 board, motor driver, and
  sensors.
- If ultrasonic sensors output 5 V echo signals, do not connect Echo directly
  to ESP32 GPIO without level shifting.
- Test motors at low speed first and keep a manual stop available.
