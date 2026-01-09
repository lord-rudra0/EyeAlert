import firebase_admin
from firebase_admin import credentials, db
import socket
import time
import os

class FirebaseManager:
    def __init__(self, actions_limit=2.0):
        self.initialized = False
        self.device_ip = self.get_ip_address()
        self.last_sent = 0
        self.limit = actions_limit # Min seconds between alerts
        
        # Try to init
        cred_path = "serviceAccountKey.json"
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://eyewatch-monitor-default-rtdb.firebaseio.com/' # User needs to set this
                })
                self.initialized = True
                print("[Firebase] Connected Successfully.")
            except Exception as e:
                print(f"[Firebase] Error: {e}")
        else:
            print("[Firebase] Mock Mode: No 'serviceAccountKey.json' found.")

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"

    def send_alert(self, status, bpm, head_pos, message):
        if time.time() - self.last_sent < self.limit:
            return # Rate limit
            
        data = {
            "timestamp": time.time(),
            "device_ip": self.device_ip,
            "status": status,
            "bpm": bpm,
            "head_pos": head_pos, # Tuple/String
            "message": message
        }
        
        self.last_sent = time.time()
        
        if self.initialized:
            try:
                ref = db.reference('alerts')
                ref.push(data)
                print(f"[Firebase] Sent: {data}")
            except Exception as e:
                print(f"[Firebase] Send Failed: {e}")
        else:
            print(f"[Firebase MOCK] Sending Logic: {data}")
