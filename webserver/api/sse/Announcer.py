import queue

# https://maxhalford.github.io/blog/flask-sse-no-deps/

class AlarmAnnouncer:
    """An announcer to be used in SSE contexts. Contains a dictionary mapping user IDs to
       instances of python standard library queue. Using queue method put_nowait resumes any
       function waiting on the queue.
    
    Attributes
    ----------
    max_size : int
        Maximum size for each queue
    listeners : dict
        Dictionary with user ID as key and a queue for that user as value
        
    Methods
    -------
    listen(user_id : int)
        Creates a new queue for this specific user
    announce_alarm(users : list, msg : str)
        For each user ID in users, put msg in that users queue. This will trigger the SSE endpoint,
        which for each user that is listening is waiting for a new message in the queue
    """
    
    def __init__(self, max_size):
        """
        Create the announcer
        
        Parameters
        ----------
        max_size : int
            maximum size for each queue
        """
        self.max_size = max_size
        self.listeners = {}
        
    def listen(self, user_id):
        """Create a new queue for this specific user, allowing it to listen to SSE messages
        
        Parameters
        ----------
        user_id : int
            unique ID of the user
            
        Returns
        -------
        A new queue for this specific user
        """
        listen_queue = queue.Queue(maxsize=self.max_size)
        
        self.listeners[user_id] = listen_queue
        
        return listen_queue
    
    def announce_alarm(self, users, msg):
        
        """For each user ID in users, put msg in its queue. This will resume any function waiting
        on any of these queues.
        
        Parameters
        ----------
        users : list
            list of user IDs
        msg : str
            a message in SSE format
        """
        
        #print (f'Users to alert: {users}')
        #print (f'Listeners: {self.listeners}')
        #print (f"Message: {msg}")
        for user in users:
            try:
                self.listeners[user].put_nowait(msg)
            except queue.Full:
                del self.listeners[user] # user used to listen but stopped listening
            except:
                print("User wasn't listening")
            
    
            