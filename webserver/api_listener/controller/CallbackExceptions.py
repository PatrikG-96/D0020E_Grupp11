from protocol.exceptions import ProtocolException

class JsonException(ProtocolException):
    """Extension of ProtocolException. A wrapper around any kind of exceptions that may occur when using the python JSON
       library to parse a string to JSON.
    """
    def __init__(self, message: str, code : int, data: str):
        """Creates the exception

        Parameters
        ----------
        message : str
            The error message for the exception
        code : int
            Error code, defined in protocol
        data : str
            The string data that caused the exception
        """
        self.data = data
        super().__init__(message, code)
        
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Data '{self.data}' could not be parsed to JSON. Failed with error: '{self.message}'."
        
class DecisionException(ProtocolException):
    
    """Extension of ProtocolException. A wrapper around any kind of exceptions that may occur when attempting to decide on an
       action for a received message.
    """
    
    def __init__(self, message: str, code : int, error: str):
        """Creates the exception

        Parameters
        ----------
        message : str
            The error message for the exception
        code : int
            Error code, defined in protocol
        error : str
            A more specific error message that describes the context where the error occured
        """
        self.error = error
        super().__init__(message, code)
        
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Failed at making decision for message: '{self.message}'. Error message: '{self.error}'."
        
class DecodeException(ProtocolException):
    """Extension of ProtocolException. A wrapper around any kind of exceptions that may occur when attemptin to decode the raw bytes
       into a utf-8 string.
    """
    def __init__(self, message: str, code: int):
        """Creates the exception

        Parameters
        ----------
        message : str
            The error message for the exception
        code : int
            Error code, defined in protocol
        """
        super().__init__(message, code)
        
    def __rep__(self):
        return f"Error code: '{self.code}'. Decoding failed with error: '{self.message}'"
     