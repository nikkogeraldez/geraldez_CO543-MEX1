Learning Outcomes
By the end of this exercise, you should be able to:
• Capture and process real-time webcam frames.
• Detect movement between consecutive frames.
• Implement state-based game logic (GREEN, RED, WARNING, DEAD, LEVEL_UP).
• Tune thresholds and timing in a noisy real-world CV setup.
• Explain design tradeoffs and failure cases.

Project Specifications
Implement a Red Light Green Light game with the following rules:
• Game starts in GREEN.
• During GREEN, player must move.
• System switches to RED after a random GREEN duration.
• During RED, player must remain still.
• If movement during RED exceeds threshold after grace window, player dies.
• If player survives RED, the game continues.
• During GREEN, if player stays still too long, show warning; if still no movement, player dies.

Technical Requirements
You must implement all of the following sections.
A. Input and Preprocessing
• Read webcam stream continuously.
• Resize frame for speed (recommended width: 640).
• Convert frames to grayscale.
• Optionally apply blur to reduce noise.
B. Motion Score
Compute motion score from frame-to-frame difference:
• diff = abs(current_gray - previous_gray)
• motion_score = mean(diff) / 255.0
• Optionally threshold binary motion mask before scoring.
C. RLGL State Machine
Required states:
• GREEN
• RED
• WARNING
• DEAD

Required timers/variables:
• green_duration (randomized)
• red_duration (randomized)
• red_grace_ms
• idle_warning_ms
• idle_death_ms
D. Rules
GREEN State
• If motion is below green_move_threshold, start/continue idle timer.
• If idle timer > idle_warning_ms: enter WARNING.
• If idle timer > idle_death_ms: DEAD.
• After green timer expires: switch to RED.
RED State
• First red_grace_ms are ignored.
• After grace, if motion > red_move_threshold(level): DEAD.
• If red timer expires without violation: success.

Suggested Baseline Parameters
Use these as starting values and tune as needed:
• green_move_threshold = 0.04
• red_move_threshold_base = 0.055
• red_grace_ms = 650
• idle_warning_ms = 1800
• idle_death_ms = 3600
• Green duration range level 1: 2600ms – 4200ms
• Red duration range level 1: 1700ms – 2900ms
