class Client:

    def __init__(self, name, uid, username, password, writer):
        self.writer = writer
        self.uid = uid
        self.name = name
        self.username = username
        self.password = password
        self.subscribed_alarms = []

    def subscribeToAlarm(self, alarm_id):
        if alarm_id not in (self.subscribed_alarms):
            self.subscribed_alarms.append(alarm_id)

    
    def getWriter(self):
        return self.writer

    def getUID(self):
        return self.uid

    def getUsername(self):
        return self.username
    
    def getName(self):
        return self.name


    
    
