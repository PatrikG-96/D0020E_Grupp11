from protocol.exceptions import ProtocolException

class JsonException(ProtocolException):
    
    def __init__(self, message: str, code : int, data: str):
        self.data = data
        super().__init__(message, code)
        
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Data '{self.data}' could not be parsed to JSON. Failed with error: '{self.message}'."
        
class DecisionException(ProtocolException):
    
    def __init__(self, message: str, code : int, error: str):
        self.error = error
        super().__init__(message, code)
        
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Failed at making decision for message: '{self.message}'. Error message: '{self.error}'."
        
class DecodeException(ProtocolException):
    
    def __init__(self, message: str, code: int):
        super().__init__(message, code)
        
    def __rep__(self):
        return f"Error code: '{self.code}'. Decoding failed with error: '{self.message}'"
     