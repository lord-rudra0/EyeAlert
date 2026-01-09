import time
import numpy as np
import config

class HeadMovementTracker:
    def __init__(self):
        self.pitch_history = []
        self.history_len = 30 # Store last ~1 second @ 30fps
        self.is_sleeping = False
        self.last_state_change = 0

    def update(self, pose):
        # pose: (pitch, yaw, roll)
        if pose is None: return False
        
        pitch, yaw, roll = pose
        self.pitch_history.append(pitch)
        if len(self.pitch_history) > self.history_len:
            self.pitch_history.pop(0)

        # Logic 1: Sustained Head Drop (Looking down significantly)
        # Note: Pitch is typically positive for looking up, negative for looking down, or vice versa depending on solver.
        # Assuming typical OpenCV solvePnP: Pitch > 0 is looking DOWN (often). Need to verify.
        # Let's assume standard: X-axis points right, Y-axis points down, Z-axis points forward.
        # Rotating around X (Pitch): Positive -> Up? No, usually Y is down.
        # Let's rely on magnitude for now or assume user calibrated.
        # Actually simplest: if ALL recent pitch values are > threshold (looking down)
        
        avg_pitch = np.mean(self.pitch_history)
        
        # Heuristic: If pitch is consistently high/low (looking down).
        # We'll assume Looking DOWN is significant deviation in one direction.
        # Let's check absolute deviation if we aren't sure of sign, OR detecting "stillness" in bad pose.
        
        is_looking_down = avg_pitch > config.SLEEP_PITCH_THRESHOLD # Adjust sign if needed
        
        # Logic 2: Nodding (Cyclic movement)
        # Check variance/oscillation
        # For simplicity, we stick to "Head Drop" = Sleeping for now.
        
        if is_looking_down:
            if time.time() - self.last_state_change > 1.0: # Debounce
                self.is_sleeping = True
        else:
            self.is_sleeping = False
            self.last_state_change = time.time()
            
        return self.is_sleeping
