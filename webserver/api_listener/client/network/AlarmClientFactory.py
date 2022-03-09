from twisted.internet.protocol import ClientFactory



class AlarmClientFactory(ClientFactory):
    
    def __init__(self):
        self.username = None
        self.password = None
        self.id = None
        self.token = None
        self.jwt = None
        
    