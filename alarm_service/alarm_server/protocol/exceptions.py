
class ProtocolException(Exception):
    
    def __init__(self, message : str, code : int):
        self.message = message
        self.code = code

class UnknownException(ProtocolException):
    
    def __init__(self, message : str, code : int):
        super().__init__(message, code)

    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Unexpected error: {self.message}"
     

class FormatException(ProtocolException):
    
    def __init__(self, message : str, code : int, type : str, data : dict):
        self.type = type
        self.data = data
        super().__init__(message, code)
        
    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Parsing '{str(self.data)}' into Type: '{self.type} failed with errors: {self.message}"
     
