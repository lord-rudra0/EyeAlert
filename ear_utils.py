# ear_utils.py
import numpy as np
import config

def calculate_eye_ear(landmarks, eye_indices, w, h):
    # Extract coordinates
    coords = []
    for idx in eye_indices:
        lm = landmarks[idx]
        coords.append(np.array([lm.x * w, lm.y * h]))

    # Vertical distances
    v1 = np.linalg.norm(coords[1] - coords[5])
    v2 = np.linalg.norm(coords[2] - coords[4])
    # Horizontal distance
    horiz = np.linalg.norm(coords[0] - coords[3])

    if horiz == 0: return 0.0
    return (v1 + v2) / (2.0 * horiz)

def get_avg_ear(landmarks, w, h):
    l_ear = calculate_eye_ear(landmarks.landmark, config.LEFT_EYE, w, h)
    r_ear = calculate_eye_ear(landmarks.landmark, config.RIGHT_EYE, w, h)
    return (l_ear + r_ear) / 2.0
