# main.py
import cv2
import config
from mp_wrapper import FaceMeshWrapper
from score_logic import ReliabilityScorer
from reaction_logic import ReactionTester
from movement_logic import HeadMovementTracker, DistractionTracker
from occlusion_logic import OcclusionDetector
from firebase_manager import FirebaseManager
from graph_renderer import TrendGraph
import ear_utils, pose_utils, visualizer, ui_renderer

def main():
    cap = cv2.VideoCapture(0)
    mesh, scorer, rectest, graph = FaceMeshWrapper(), ReliabilityScorer(), ReactionTester(), TrendGraph()
    
    # New Detectors
    move_tracker = HeadMovementTracker()
    occ_detector = OcclusionDetector()
    dist_tracker = DistractionTracker()
    blink_detector = ear_utils.BlinkDetector()
    
    # Firebase
    fb_manager = FirebaseManager()

    while True:
        success, img = cap.read()
        if not success: continue
        h, w, _ = img.shape
        results = mesh.process_frame(img)
        
        ear, pose = 0.0, None
        
        # Detection States
        is_sleeping = False
        is_mask = False
        is_sunglasses = False
        mask_val = 0.0
        direction = "UNKNOWN"
        is_distracted = False
        bpm = 0
        
        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0]
            visualizer.draw_mesh(img, results)
            ear = ear_utils.get_avg_ear(lm, w, h)
            pose, vec = pose_utils.estimate_head_pose(lm, w, h)
            if vec[0] is not None: visualizer.draw_pose_line(img, lm, vec[0], vec[1], w, h)
            
            # Update Trackers
            is_sleeping = move_tracker.update(pose)
            is_mask, is_sunglasses, mask_val = occ_detector.update(img, results, w, h)
            
            # Distraction Logic
            direction = dist_tracker.get_direction(pose)
            is_distracted = dist_tracker.update(direction)
            
            # Blink Logic
            bpm = blink_detector.update(ear)

        score = scorer.update(ear, pose, is_sunglasses=is_sunglasses)
        
        # Trigger Sleep Alert if score is low
        if score < 50.0: is_sleeping = True
        
        # Reaction Test (Disabled)
        # if rectest.should_trigger(): pass
        # if rectest.check_timeout(): scorer.apply_penalty(config.REACTION_PENALTY)
        # if rectest.active: ui_renderer.draw_alert(img, w, h)

        # UI
        txt, col = ui_renderer.get_status_color(score)
        ui_renderer.draw_hud(img, score, txt, col, ear, pose)
        ui_renderer.draw_occlusion_alerts(img, w, h, is_sleeping, is_mask, is_sunglasses, debug_val=mask_val)
        ui_renderer.draw_bpm(img, bpm)
        
        graph.update(score, col)
        graph.draw(img, 10, h-110)

        ui_renderer.draw_direction(img, direction)
        
        # Actions & Alerts
        alert_msg = ""
        if is_sleeping: 
             alert_msg = "SLEEPING"
        elif is_distracted:
             alert_msg = "DISTRACTED"
             ui_renderer.draw_distraction_alert(img, w, h)
             
        if alert_msg:
             fb_manager.send_alert(alert_msg, bpm, str(direction), f"Score: {int(score)}")

        cv2.imshow("EyeAlert", img)
        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'): break
        # if key == 32: 
        #     lat = rectest.register_input()
        #     if lat: scorer.apply_penalty(-5.0) # Bonus

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__": main()
