
import cv2
import numpy as np
import time
import random

# ========================
# CONFIGURATION
# ========================
FRAME_WIDTH = 640

green_move_threshold = 0.04
red_move_threshold_base = 0.055

red_grace_ms = 650
idle_warning_ms = 1800
idle_death_ms = 3600

green_min = 2600
green_max = 4200
red_min = 1700
red_max = 2900

# ========================
# STATES
# ========================
GREEN = "GREEN"
RED = "RED"
WARNING = "WARNING"
DEAD = "DEAD"

state = GREEN

# ========================
# TIMERS
# ========================
state_start_time = time.time()
idle_start_time = None

def current_ms():
    return int(time.time() * 1000)

def random_green_duration():
    return random.randint(green_min, green_max)

def random_red_duration():
    return random.randint(red_min, red_max)

green_duration = random_green_duration()
red_duration = random_red_duration()

# ========================
# VIDEO SETUP
# ========================
cap = cv2.VideoCapture(0)
prev_gray = None

print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize
    scale = FRAME_WIDTH / frame.shape[1]
    frame = cv2.resize(frame, (FRAME_WIDTH, int(frame.shape[0] * scale)))

    # Preprocess
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Motion score
    motion_score = 0

    if prev_gray is not None:
        diff = cv2.absdiff(gray, prev_gray)
        motion_score = np.mean(diff) / 255.0

    prev_gray = gray.copy()

    now_ms = current_ms()
    elapsed_state = (time.time() - state_start_time) * 1000

    # ========================
    # STATE MACHINE
    # ========================

    if state == GREEN or state == WARNING:

        # Check motion
        if motion_score < green_move_threshold:
            if idle_start_time is None:
                idle_start_time = now_ms
            idle_time = now_ms - idle_start_time

            if idle_time > idle_warning_ms:
                state = WARNING

            if idle_time > idle_death_ms:
                state = DEAD
        else:
            idle_start_time = None
            state = GREEN

        # Transition to RED
        if elapsed_state > green_duration:
            state = RED
            state_start_time = time.time()
            red_start_ms = current_ms()
            red_duration = random_red_duration()
            idle_start_time = None

    elif state == RED:

        red_elapsed = now_ms - red_start_ms

        # Grace period
        if red_elapsed > red_grace_ms:
            if motion_score > red_move_threshold_base:
                state = DEAD

        # Survived RED
        if red_elapsed > red_duration:
            state = GREEN
            state_start_time = time.time()
            green_duration = random_green_duration()
            idle_start_time = None

    # ========================
    # DISPLAY
    # ========================
    color = (0, 255, 0)

    if state == GREEN:
        color = (0, 255, 0)
    elif state == RED:
        color = (0, 0, 255)
    elif state == WARNING:
        color = (0, 255, 255)
    elif state == DEAD:
        color = (0, 0, 255)

    cv2.putText(frame, f"STATE: {state}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.putText(frame, f"Motion: {motion_score:.4f}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("RLGL CV Game", frame)

    if state == DEAD:
        cv2.putText(frame, "YOU DIED!", (200, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.imshow("RLGL CV Game", frame)
        cv2.waitKey(2000)
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
