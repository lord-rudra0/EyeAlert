import time
import collections
import numpy as np

class ReliabilityScorer:
    def __init__(self):
        self.score = 100.0
        self.ear_history = collections.deque(maxlen=100) # ~3 seconds at 30fps
        self.blink_count = 0
        self.last_blink_time = time.time()
        
        # Thresholds
        self.EAR_THRESHOLD = 0.22  # Below this is considered closed
        self.POSE_YAW_THRESHOLD = 20 # Degrees
        self.POSE_PITCH_THRESHOLD = 15 # Degrees
        
        # Scoring weights/penalties
        self.DECAY_RATE_EYES = 2.0
        self.DECAY_RATE_POSE = 1.0
        self.RECOVERY_RATE = 0.5
        self.REACTION_PENALTY = 20.0 # Instant drop
        
    def register_reaction(self, latency):
        """
        Updates score based on reaction time latency (seconds).
        Target < 0.5s.
        """
        if latency > 1.0:
            self.score = max(0.0, self.score - self.REACTION_PENALTY)
        elif latency > 0.5:
            self.score = max(0.0, self.score - (self.REACTION_PENALTY / 2))
        else:
             # Reward slightly
             self.score = min(100.0, self.score + 5.0)
        
    def update(self, ear, head_pose):
        """
        Updates the reliability score based on current frame data.
        ear: float, avg eye aspect ratio
        head_pose: tuple (pitch, yaw, roll) in degrees
        """
        self.ear_history.append(ear)
        
        penalty = 0.0
        is_attentive = True

        # Check Eyes
        if ear < self.EAR_THRESHOLD:
            penalty += self.DECAY_RATE_EYES
            is_attentive = False
            
        # Check Head Pose
        # head_pose is (pitch, yaw, roll)
        if head_pose is not None:
            pitch, yaw, roll = head_pose
            if abs(yaw) > self.POSE_YAW_THRESHOLD or abs(pitch) > self.POSE_PITCH_THRESHOLD:
                penalty += self.DECAY_RATE_POSE
                is_attentive = False

        # Apply Score Changes
        if not is_attentive:
            self.score = max(0.0, self.score - penalty)
        else:
            self.score = min(100.0, self.score + self.RECOVERY_RATE)
            
        return self.score

    def get_status(self):
        """Returns a string status based on score."""
        if self.score > 80:
            return "Reliable", (0, 255, 0)
        elif self.score > 50:
            return "Degrading", (0, 255, 255)
        else:
            return "UNSAFE", (0, 0, 255)
