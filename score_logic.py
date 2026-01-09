# score_logic.py
import config

class ReliabilityScorer:
    def __init__(self):
        self.score = 100.0

    def update(self, ear, head_pose):
        penalty = 0.0
        is_attentive = True

        if ear < config.EAR_THRESHOLD:
            penalty += config.DECAY_RATE_EYES
            is_attentive = False
            
        if head_pose:
            p, y, r = head_pose
            if abs(y) > config.POSE_YAW_THRESHOLD or abs(p) > config.POSE_PITCH_THRESHOLD:
                penalty += config.DECAY_RATE_POSE
                is_attentive = False

        if not is_attentive:
            self.score = max(0.0, self.score - penalty)
        else:
            self.score = min(100.0, self.score + config.RECOVERY_RATE)
        return self.score

    def apply_penalty(self, points):
        self.score = max(0.0, self.score - points)
