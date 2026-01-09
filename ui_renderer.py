# ui_renderer.py
import cv2
import config

def draw_hud(image, score, status_text, status_color, ear, pose):
    h, w = image.shape[:2]
    # Status Bar
    cv2.rectangle(image, (0, 0), (w, 50), (30, 30, 30), -1)
    cv2.putText(image, f"Score: {int(score)}%", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
    cv2.putText(image, status_text, (250, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

    # Metrics
    cv2.putText(image, f"EAR: {ear:.2f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_GREEN, 2)
    if pose is not None:
        cv2.putText(image, f"Y: {int(pose[1])} P: {int(pose[0])}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_GREEN, 2)

def draw_alert(image, w, h):
    cv2.putText(image, "PRESS SPACE!", (w//2-150, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, config.COLOR_RED, 4)

def draw_occlusion_alerts(image, w, h, sleeping, mask, sunglasses, debug_val=0.0):
    y_offset = 150
    if sleeping:
        cv2.putText(image, "SLEEPING!", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_RED, 2)
        y_offset += 30

def draw_direction(image, direction):
    h = image.shape[0]
    cv2.putText(image, f"Looking: {direction}", (10, h-80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, config.COLOR_YELLOW, 2)

def draw_distraction_alert(image, w, h):
    cv2.putText(image, "FOCUS ON ROAD!", (w//2-200, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, config.COLOR_RED, 4)

def get_status_color(score):
    if score > 80: return "Reliable", config.COLOR_GREEN
    if score > 50: return "Degrading", config.COLOR_YELLOW
    return "SLEEPING", config.COLOR_RED
