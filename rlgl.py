
import cv2
import numpy as np
import time
import random

# =============================
# PARAMETERS
# =============================
GREEN_MOVE_THRESHOLD = 0.04
RED_MOVE_THRESHOLD = 0.055

RED_GRACE_MS = 650
IDLE_WARNING_MS = 1800
IDLE_DEATH_MS = 3600

GREEN_MIN = 2.6
GREEN_MAX = 4.2

RED_MIN = 1.7
RED_MAX = 2.9

# =============================
# STATES
# =============================
GREEN = "GREEN"
RED = "RED"
WARNING = "WARNING"
DEAD = "DEAD"

# =============================
# FUNCTIONS
# =============================
def compute_motion(prev, curr):
    diff = cv2.absdiff(prev, curr)
    return np.mean(diff) / 255.0

def draw_text(frame, text, y, color=(255, 255, 255), scale=0.7):
    cv2.putText(frame, text, (20, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2)

# =============================
# MAIN PROGRAM
# =============================
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return

    state = GREEN
    prev_gray = None

    state_start = time.time()
    idle_start = None
    dead_reason = ""

    green_duration = random.uniform(GREEN_MIN, GREEN_MAX)
    red_duration = random.uniform(RED_MIN, RED_MAX)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        motion_score = 0

        if prev_gray is not None:
            motion_score = compute_motion(prev_gray, gray)

        prev_gray = gray

        now = time.time()
        elapsed = now - state_start
        elapsed_ms = elapsed * 1000

        # =============================
        # STATE LOGIC
        # =============================
        if state == GREEN:
            color = (0, 255, 0)

            if motion_score < GREEN_MOVE_THRESHOLD:
                if idle_start is None:
                    idle_start = now

                idle_time = (now - idle_start) * 1000

                if idle_time > IDLE_DEATH_MS:
                    state = DEAD
                    dead_reason = "Stayed still too long"
                elif idle_time > IDLE_WARNING_MS:
                    state = WARNING
            else:
                idle_start = None

            if elapsed > green_duration:
                state = RED
                state_start = now
                red_duration = random.uniform(RED_MIN, RED_MAX)

        elif state == WARNING:
            color = (0, 255, 255)

            if motion_score >= GREEN_MOVE_THRESHOLD:
                state = GREEN
                idle_start = None
            else:
                idle_time = (now - idle_start) * 1000
                if idle_time > IDLE_DEATH_MS:
                    state = DEAD
                    dead_reason = "Ignored warning"

        elif state == RED:
            color = (0, 0, 255)

            if elapsed_ms > RED_GRACE_MS:
                if motion_score > RED_MOVE_THRESHOLD:
                    state = DEAD
                    dead_reason = "Moved during RED"

            if elapsed > red_duration:
                state = GREEN
                state_start = now
                green_duration = random.uniform(GREEN_MIN, GREEN_MAX)

        elif state == DEAD:
            color = (0, 0, 0)

        # =============================
        # DISPLAY
        # =============================
        draw_text(frame, f"State: {state}", 40, color, 1)
        draw_text(frame, f"Motion: {motion_score:.4f}", 80)

        if state == DEAD:
            draw_text(frame, f"Game Over: {dead_reason}", 120, (0, 0, 255))

        cv2.imshow("RLGL Game", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
