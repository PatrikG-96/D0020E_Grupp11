
from threading import Thread
import time

class Timer(Thread):
    
    def __init__(self, seconds, callback, message):
        Thread.__init__(self)
        self.cb = callback
        self.message = message
        self.seconds = seconds
        self.running = False
        
    def start(self):
        print("starting")
        self.running = True
        super().start()
        
    def stop(self):
        print("stopping")
        self.running = False
        
    def run(self):
        secs = self.seconds
        while secs > 0 and self.running:
            time.sleep(1)
            secs-=1
        print("out of loop")
        if self.running:    
            self.cb(self.message)
    
        