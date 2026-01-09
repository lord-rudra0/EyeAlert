# reaction_logic.py
import time
import config

class ReactionTester:
    def __init__(self):
        self.last_test = time.time()
        self.active = False
        self.start_time = 0

    def should_trigger(self):
        if not self.active and (time.time() - self.last_test > 15):
            self.active = True
            self.start_time = time.time()
            return True
        return False

    def check_timeout(self):
        if self.active and (time.time() - self.start_time > 2.0):
            self.active = False
            self.last_test = time.time()
            return True # Timeout happened
        return False

    def register_input(self):
        if self.active:
            latency = time.time() - self.start_time
            self.active = False
            self.last_test = time.time()
            return latency
        return None
