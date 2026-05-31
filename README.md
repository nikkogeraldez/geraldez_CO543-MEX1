
# Red Light Green Light (RLGL) – Computer Vision Project

## Overview
This project implements a **Red Light Green Light game** using webcam-based motion detection with OpenCV.

The system analyzes frame differences to determine whether the player is moving or staying still.

---

## Features
- Real-time webcam capture
- Motion detection using frame differencing
- State machine:
  - GREEN (move)
  - RED (stay still)
  - WARNING
  - DEAD (game over)
- Idle detection and penalties
- Randomized timing for realism

---

## Algorithm

### Motion Score
``
