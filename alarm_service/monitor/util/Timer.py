import logging
from threading import Thread
import time

log = logging.getLogger()

class Timer(Thread):
    
    """
    A Timer that runs in a separate thread and will trigger a callback when it runs out.
    It does not take into account race conditions and such, so that will need to be handled
    in the callback function provided.
    
    Attributes
    ----------
    parent : str
        The ID of the entity that started the timer
    seconds : int
        Amount of seconds the timer should run
    callback : function
        Function to be called at the end of the timer. Must take one argument.
    message : ...
        A message that will be passed as the argument to the callback function
        
    Methods
    -------
    start()
        Starts the timer
    stop()
        Stops the timer
    run()
        The actual timer function
    """
    
    def __init__(self, parent, seconds, callback, message):
        """
        Create the timer
        
        Parameters
        ----------
        parent : str
            The ID of the entity that started the timer
        seconds : int
            Amount of seconds the timer should run
        callback : function
            Function to be called at the end of the timer. Must take one argument.
        message : ...
            A message that will be passed as the argument to the callback function
        """
        Thread.__init__(self)
        self.parent = parent
        self.cb = callback
        self.message = message
        self.seconds = seconds
        self.running = False
        
    def start(self):
        """
        Start the timer.
        """
        log.info(f"(Timer:{self.parent}) Timer started: {self.seconds} seconds.")
        self.running = True
        super().start()
        
    def stop(self):
        """
        Stop the timer.
        """
        log.info(f"(Timer:{self.parent}) Timer stopped.")
        self.running = False
        
    def run(self):
        """
        Function to run in thread.
        """
        secs = self.seconds
        while secs > 0 and self.running:
            time.sleep(1)
            secs-=1
        if self.running:
            log.info(f"(Timer:{self.parent}) Timer completed.")    
            self.cb(self.message)
    
        