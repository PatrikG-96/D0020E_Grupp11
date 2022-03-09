import logging
from threading import Thread
import time

log = logging.getLogger()

class Timer(Thread):
    
    def __init__(self, parent, seconds, callback, message):
        Thread.__init__(self)
        self.parent = parent
        self.cb = callback
        self.message = message
        self.seconds = seconds
        self.running = False
        
    def start(self):
        log.info(f"(Timer:{self.parent}) Timer started: {self.seconds} seconds.")
        self.running = True
        super().start()
        
    def stop(self):
        log.info(f"(Timer:{self.parent}) Timer stopped.")
        self.running = False
        
    def run(self):
        secs = self.seconds
        while secs > 0 and self.running:
            time.sleep(1)
            secs-=1
        if self.running:
            log.info(f"(Timer:{self.parent}) Timer completed.")    
            self.cb(self.message)
    
        