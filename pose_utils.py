# pose_utils.py
import cv2
import numpy as np

def estimate_head_pose(landmarks, w, h):
    # Nose, Chin, L-Eye-L, R-Eye-R, L-Mouth, R-Mouth
    ids = [1, 152, 263, 33, 291, 61]
    img_pts = []
    for idx in ids:
        lm = landmarks.landmark[idx]
        img_pts.append([lm.x * w, lm.y * h])
    
    img_pts = np.array(img_pts, dtype=np.float64)
    model_pts = np.array([
        (0.0, 0.0, 0.0), (0.0, -330.0, -65.0), (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0), (-150.0, -150.0, -125.0), (150.0, -150.0, -125.0)
    ])
    
    cam_matrix = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype="double")
    dist = np.zeros((4, 1))

    success, rvec, tvec = cv2.solvePnP(model_pts, img_pts, cam_matrix, dist)
    if not success: return None, None
    
    rmat, _ = cv2.Rodrigues(rvec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    return angles, (rvec, tvec) # angles: [pitch, yaw, roll]
