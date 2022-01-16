
class FullMessage:

    def __init__(self):
        self.header = None
        self.message = None

    def setHeader(self, header):
        self.header = header

    def setMessage(self, message):
        self.message = message

    def getHeader(self):
        return self.header

    def getMessage(self):
        return self.message