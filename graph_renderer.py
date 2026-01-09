# graph_renderer.py
import cv2
import numpy as np

class TrendGraph:
    def __init__(self):
        self.canvas = np.zeros((100, 400, 3), dtype=np.uint8)

    def update(self, score, color):
        self.canvas[:, :-1] = self.canvas[:, 1:] # Shift
        self.canvas[:, -1] = (0,0,0)
        
        val = int(100 - score)
        cv2.line(self.canvas, (398, val), (399, val), color, 2)

    def draw(self, image, x, y):
        h, w = self.canvas.shape[:2]
        # Check bounds
        if y+h > image.shape[0] or x+w > image.shape[1]: return
        
        image[y:y+h, x:x+w] = self.canvas
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255), 1)
