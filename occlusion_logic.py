import cv2
import numpy as np
import config

class OcclusionDetector:
    def __init__(self):
        self.mask_detected = False
        self.sunglasses_detected = False
        self.frame_count = 0

    def get_roi_stats(self, frame, landmarks, indices, w, h):
        # Extract pixels for ROI
        pts = []
        for idx in indices:
            lm = landmarks.landmark[idx]
            pts.append([int(lm.x * w), int(lm.y * h)])
        
        if not pts: return None, None
        
        pts = np.array(pts)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        # Convex hull for area
        hull = cv2.convexHull(pts)
        cv2.fillConvexPoly(mask, hull, 255)
        
        mean_val = cv2.mean(frame, mask=mask)[:3] # BGR
        return mean_val, hull

    def update(self, frame, results, w, h):
        self.frame_count += 1
        if self.frame_count % 10 != 0: # Run every 10 frames
            return self.mask_detected, self.sunglasses_detected, 0.0
            
        if not results.multi_face_landmarks:
            return False, False
            
        lm = results.multi_face_landmarks[0]
        
        # Reference Skin (Cheeks - better than forehead due to hair/lighting)
        l_cheek_val, _ = self.get_roi_stats(frame, lm, config.LEFT_CHEEK, w, h)
        r_cheek_val, _ = self.get_roi_stats(frame, lm, config.RIGHT_CHEEK, w, h)
        
        if l_cheek_val is None or r_cheek_val is None: return False, False, 0.0
        
        # Average cheeks
        skin_val = (np.array(l_cheek_val) + np.array(r_cheek_val)) / 2.0
        skin_brightness = np.mean(skin_val)
        
        # Check Sunglasses (Eyes vs Skin)
        # Average both eyes
        l_eye_val, _ = self.get_roi_stats(frame, lm, config.LEFT_EYE, w, h)
        r_eye_val, _ = self.get_roi_stats(frame, lm, config.RIGHT_EYE, w, h)
        
        if l_eye_val is not None and r_eye_val is not None:
            eyes_brightness = (np.mean(l_eye_val) + np.mean(r_eye_val)) / 2.0
            # Sunglasses: Eyes much darker than skin
            if (skin_brightness - eyes_brightness) > config.OCCLUSION_THRESHOLD_BRIGHTNESS:
                self.sunglasses_detected = True
            else:
                self.sunglasses_detected = False
                
        # Check Mask (Mouth/Nose vs Skin)
        mouth_val, _ = self.get_roi_stats(frame, lm, config.MOUTH_INNER, w, h)
        color_diff = 0.0
        if mouth_val is not None:
            # Mask: Significant Color/Brightness difference
            color_diff = np.linalg.norm(np.array(skin_val) - np.array(mouth_val))
            if color_diff > config.OCCLUSION_THRESHOLD_COLOR:
                 self.mask_detected = True
            else:
                 self.mask_detected = False

        return self.mask_detected, self.sunglasses_detected, color_diff
