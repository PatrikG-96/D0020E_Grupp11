from twisted.internet.protocol import ClientFactory



class AlarmClientFactory(ClientFactory):
    
    """Simple class intended to be abstract. Contains fields that are required for performing the connection
    process to alarm server, but none of the logic that may be required. Subclass this for a functioning Factory
    to be used in communication with alarm server.
    """
    
    def __init__(self):
        self.username = None
        self.password = None
        self.id = None
        self.token = None
        self.jwt = None
        
    