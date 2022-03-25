import socket
from threading import Thread
from util.Timer import Timer
import logging

log = logging.getLogger()

class Client(Thread):
    
    """
    Extension of threading.Thread. Represents a simple client that runs in its own thread. It will simply
    send a message then wait for a response until it either receives it or times out. The thread is then stopped.
    
    Attributes
    ----------
    id : str
        id of the entity that created the message, for example a sensor.
    addr : str
        IP address of the server to connect to
    port : int
        port of the server to connect to
    timeout : int
        timeout in seconds
    message : bytes
        string message encode into bytes
    timer : Timer
        timer that stops the thread after timeout seconds
        
    Methods
    -------
    run()
        Start the thread
    cancel()
        Stop the thread
    """
    
    def __init__(self, id, addr, port, message, timeout):
        """
        Create the client thread
        
        Parameters
        ----------
        id : str
            id of the entity that created the message, for example a sensor.
        addr : str
            IP address of the server to connect to
        port : int
            port of the server to connect to
        timeout : int
            timeout in seconds
        message : str
            string message to send
        """
        Thread.__init__(self)
        self.id = id
        self.daemon = True
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = message.encode()
        self.timeout = timeout
        self.timer = Timer(str(self), self.timeout, self.cancel, None)
        
    def run(self):
        """
        Function to run in the thread.
        """
        try:
            self.socket.connect((self.addr, self.port))
            self.socket.sendall(self.message)
            
            log.info(f"(Client:{self.id}) Message sent to server")
            
            self.timer.start()
            
            data = self.socket.recv(512)
            
            log.info(f"(Client:{self.id}) Reponse received: {data.decode()}")
            
            self.timer.stop()
            
            
        except Exception as e:
            log.warning(f"(Client:{self.id}) Error: {e}")
            self.socket.close()
        
        self.socket.close()
        
    def cancel(self, msg):
        """
        Stop the thread
        """
        log.info(f"(Client:{self.id}) Timed out")
        self.socket.close()
        
    def __str__(self):
        return f"(Client:{self.id})"