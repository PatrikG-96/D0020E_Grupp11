import socket
from threading import Thread
from util.Timer import Timer
import logging

log = logging.getLogger()

class Client(Thread):
    
    def __init__(self, id, addr, port, message, timeout):
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
        log.info(f"(Client:{self.id}) Timed out")
        self.socket.close()
        
    def __str__(self):
        return f"(Client:{self.id})"