# config.py

# Camera / Frame
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Reliability Logic
EAR_THRESHOLD = 0.22
POSE_YAW_THRESHOLD = 20
POSE_PITCH_THRESHOLD = 15

# Scoring Rates
DECAY_RATE_EYES = 0.5
DECAY_RATE_POSE = 0.1
RECOVERY_RATE = 0.5
REACTION_PENALTY = 20.0

# Colors (BGR)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)

# Eye Indices (MediaPipe)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# ROI Indices (Simplified)
# Forehead: measure skin color
FOREHEAD = [10, 151, 9] 
# Cheeks: measure skin color
LEFT_CHEEK = [330, 347]
RIGHT_CHEEK = [101, 118]
# Nose tip
NOSE_TIP = [1]
# Mouth area for mask
MOUTH_INNER = [13, 14, 312, 317, 82, 87]

# Detection Thresholds
SLEEP_PITCH_THRESHOLD = 5.0 # Looking down > 10 degrees (adjust actual value after testing)
NOD_AMPLITUDE = 5.0
OCCLUSION_THRESHOLD_COLOR = 60.0 # BGR diff
OCCLUSION_THRESHOLD_BRIGHTNESS = 40.0
DISTRACTION_TIMEOUT = 3.0
