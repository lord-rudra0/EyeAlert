import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Indices for EAR (based on MediaPipe 468/478 mesh)
        # Left eye: [362, 385, 387, 263, 373, 380]
        # Right eye: [33, 160, 158, 133, 153, 144]
        # Note: These are standard approximate indices for 6-point EAR.
        # MediaPipe refined mesh provides iris landmarks too, but we'll use the lid contours.
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]

    def process(self, image):
        """
        Processes the image and returns the face landmarks.
        Image should be BGR (standard OpenCV).
        """
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.face_mesh.process(image_rgb)
        image_rgb.flags.writeable = True
        
        return results

    def calculate_ear(self, landmarks, eye_indices, frame_width, frame_height):
        """
        Calculates Eye Aspect Ratio for a single eye.
        landmarks: NormalizedLandmarkList
        eye_indices: list of 6 indices
        """
        # Extract coordinates
        coords = []
        for idx in eye_indices:
            lm = landmarks[idx]
            coords.append(np.array([lm.x * frame_width, lm.y * frame_height]))

        # Vertical distances
        v1 = np.linalg.norm(coords[1] - coords[5])
        v2 = np.linalg.norm(coords[2] - coords[4])

        # Horizontal distance
        h = np.linalg.norm(coords[0] - coords[3])

        if h == 0:
            return 0.0

        ear = (v1 + v2) / (2.0 * h)
        return ear

    def get_avg_ear(self, landmarks, frame_width, frame_height):
        """Calculates average EAR for both eyes."""
        left_ear = self.calculate_ear(landmarks.landmark, self.LEFT_EYE, frame_width, frame_height)
        right_ear = self.calculate_ear(landmarks.landmark, self.RIGHT_EYE, frame_width, frame_height)
        return (left_ear + right_ear) / 2.0

    def draw_landmarks(self, image, results):
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                    
    def estimate_head_pose(self, landmarks, frame_width, frame_height):
        """
        Estimates head pose (pitch, yaw, roll) using solvePnP.
        """
        img_pts = []
        # Selected landmarks for PnP: Nose tip, Chin, Left Eye Left Corner, Right Eye Right Corner, Left Mouth Corner, Right Mouth Corner
        # Mesh indices: 1, 152, 263, 33, 291, 61
        ids = [1, 152, 263, 33, 291, 61] 
        
        for idx in ids:
            lm = landmarks.landmark[idx]
            img_pts.append([lm.x * frame_width, lm.y * frame_height])
        
        img_pts = np.array(img_pts, dtype=np.float64)

        # Generic 3D model points
        model_pts = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ])

        # Camera internals
        focal_length = frame_width
        center = (frame_width / 2, frame_height / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype = "double"
        )
        dist_coeffs = np.zeros((4, 1)) # Assuming no lens distortion

        success, rotation_vector, translation_vector = cv2.solvePnP(model_pts, img_pts, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

        if not success:
            return None, None

        # Project a 3D point (standard forward) to see where it lands
        # (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

        # Calculate Euler angles
        rmat, jac = cv2.Rodrigues(rotation_vector)
        # angles: [pitch, yaw, roll]
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

        # angles: [pitch, yaw, roll]
        return angles, (rotation_vector, translation_vector)
