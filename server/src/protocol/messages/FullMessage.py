
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

    @staticmethod
    def build(header, message):
        msg = FullMessage()
        msg.setHeader(header)
        msg.setMessage(message)
        return msg

    def __str__(self):
        return str(self.header) + ";" + str(self.message)