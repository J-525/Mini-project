# USB Attack Detection System

## Overview
This project presents a behavior-based USB attack detection system designed to identify malicious activities such as BadUSB and HID-based keystroke injection attacks. Traditional security solutions often fail to detect such attacks because they operate at the hardware or firmware level and do not involve malicious files.

The proposed system monitors USB device insertion, captures keystroke activity in real time, and analyzes typing behavior to detect anomalies. A risk scoring mechanism is used to identify suspicious activity and generate alerts.

---

## Features
- Real-time USB device detection using pyudev
- Identification of Human Interface Devices (HID)
- Keystroke monitoring using evdev
- Behavior analysis based on typing speed, delay, and frequency
- Risk scoring mechanism for anomaly detection
- Alert generation and logging of suspicious activity
- Lightweight and non-intrusive monitoring system

---

## Technologies Used
- Programming Language: Python 3
- Operating System: Linux (Ubuntu / Arch Linux)
- Libraries:
  - pyudev (for USB detection)
  - evdev (for input event monitoring)

---

## System Architecture
The system consists of the following modules:
1. USB Detection Module
2. HID Identification Module
3. Keystroke Monitoring Module
4. Behavior Analysis Module
5. Risk Scoring Module
6. Alert and Logging Module

---

## How It Works
1. The system detects USB insertion events using pyudev.
2. It identifies whether the device is a HID (keyboard/mouse).
3. Keystroke events are captured in real time.
4. The system analyzes typing patterns such as speed and delay.
5. A risk score is calculated based on predefined thresholds.
6. If the risk score exceeds a limit, an alert is generated.

---

## Installation

### Prerequisites
- Linux system (recommended)
- Python 3.x installed

### Install Required Libraries
```bash
pip install -r requirements.txt
