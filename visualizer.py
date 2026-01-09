# visualizer.py
import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_fm = mp.solutions.face_mesh

def draw_mesh(image, results):
    if not results.multi_face_landmarks: return
    for lm_list in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image, landmark_list=lm_list,
            connections=mp_fm.FACEMESH_TESSELATION,
            connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style())

def draw_pose_line(image, landmarks, rvec, tvec, w, h):
    cam_matrix = np.array([[w, 0, w/2], [0, w, h/2], [0, 0, 1]], dtype="double")
    dist = np.zeros((4, 1))
    
    nose_end, _ = cv2.projectPoints(np.array([(0.0, 0.0, 500.0)]), rvec, tvec, cam_matrix, dist)
    
    p1 = (int(landmarks.landmark[1].x * w), int(landmarks.landmark[1].y * h))
    p2 = (int(nose_end[0][0][0]), int(nose_end[0][0][1]))
    cv2.line(image, p1, p2, (255, 0, 0), 2)
