import queue
# https://maxhalford.github.io/blog/flask-sse-no-deps/

class AlarmAnnouncer:
    
    def __init__(self, max_size):
        self.max_size = max_size
        self.listeners = {}
        
    def listen(self, user_id):
        
        listen_queue = queue.Queue(maxsize=self.max_size)
        
        self.listeners[user_id] = listen_queue
        
        return listen_queue
    
    def announce_alarm(self, users, msg):
        print (f'Users to alert: {users}')
        print (f'Listeners: {self.listeners}')
        print (f"Message: {msg}")
        for user in users:
            try:
                self.listeners[user].put_nowait(msg)
            except queue.Full:
                del self.listeners[user] # user used to listen but stopped listening
            except:
                print("it went to shit")
                pass # the user wasnt listening
            
    
            