import socket
from threading import Thread
from util.Timer import Timer

class Client(Thread):
    
    def __init__(self, addr, port, message, timeout):
        Thread.__init__(self)
        self.daemon = True
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message = message.encode()
        self.timeout = timeout
        self.timer = Timer(self.timeout, self.cancel, "Hej")
        
    def run(self):
        try:
            self.socket.connect((self.addr, self.port))
            
            print("sending")
            self.socket.sendall(self.message)
            
            self.timer.start()
            print("receiving")
            data = self.socket.recv(512)
            
            self.timer.stop()
            
            print(data.decode())
            
        except Exception as e:
            print(f"shit: {e}")
            self.socket.close()
        
        self.socket.close()
        
    def cancel(self, msg):
        print("canceled")
        self.socket.close()