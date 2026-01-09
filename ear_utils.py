# ear_utils.py
import config
import math
import numpy as np
import time

def get_eye_ear(landmarks, indices):
    # Calculate EAR
    p2 = [landmarks.landmark[indices[1]].x, landmarks.landmark[indices[1]].y]
    p6 = [landmarks.landmark[indices[5]].x, landmarks.landmark[indices[5]].y]
    p3 = [landmarks.landmark[indices[2]].x, landmarks.landmark[indices[2]].y]
    p5 = [landmarks.landmark[indices[4]].x, landmarks.landmark[indices[4]].y]
    p1 = [landmarks.landmark[indices[0]].x, landmarks.landmark[indices[0]].y]
    p4 = [landmarks.landmark[indices[3]].x, landmarks.landmark[indices[3]].y]

    def dist(a, b): return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    vertical = (dist(p2, p6) + dist(p3, p5))
    horizontal = dist(p1, p4) * 2.0 # avoid div by zero
    if horizontal == 0: return 0.0
    return vertical / horizontal

def get_avg_ear(landmarks, w, h):
    l_ear = get_eye_ear(landmarks, config.LEFT_EYE)
    r_ear = get_eye_ear(landmarks, config.RIGHT_EYE)
    return (l_ear + r_ear) / 2.0

class BlinkDetector:
    def __init__(self):
        self.blinks = 0
        self.blink_start_time = None
        self.bpm_window = [] # List of timestamps
        self.eye_closed = False

    def update(self, ear):
        now = time.time()
        # Clean old timestamps (>60s)
        self.bpm_window = [t for t in self.bpm_window if now - t <= 60.0]
        
        if ear < config.EAR_THRESHOLD:
            if not self.eye_closed:
                self.eye_closed = True
        else:
            if self.eye_closed:
                self.eye_closed = False
                self.blinks += 1
                self.bpm_window.append(now)
        
        return len(self.bpm_window)
