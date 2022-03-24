
class ProtocolException(Exception):
    
    """
    Generic parent class of protocol exceptions.
    
    Attributes
    ----------
    message : str
        The error message of the exception
    code : int
        The error code of the situation
    """
    
    def __init__(self, message : str, code : int):
        """
        Creates the exception

        Parameters
        ----------
        message : str
            The error message of the exception
        code : int
            The error code of the situation
        """
        self.message = message
        self.code = code

class UnknownException(ProtocolException):
    
    """
    Extension of ProtocolException. Indicates that an unknown exception has occured.
    """
    
    def __init__(self, message : str, code : int):
        """
        Creates the exception

        Parameters
        ----------
        message : str
            The error message of the exception
        code : int
            The error code of the situation
        """
        super().__init__(message, code)

    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Unexpected error: {self.message}"
     

class FormatException(ProtocolException):
    
    """
    Extension of ProtocolException. Indicates that there was an issue with the format of a protocol message.
    
    Attributes
    ----------
    type : str
        The message type that caused the exception
    data : dict
        The message that caused the exception, in JSON format 
    """
    
    def __init__(self, message : str, code : int, type : str, data : dict):
        """
        Creates the exception

        Parameters
        ----------
        message : str
            The error message of the exception
        code : int
            The error code of the situation
        type : str
            The message type that caused the exception
        data : dict
            The message that caused the exception, in JSON format 
        """
        self.type = type
        self.data = data
        super().__init__(message, code)
        
    
    def __repr__(self) -> str:
        return f"Error code: '{self.code}'. Parsing '{str(self.data)}' into Type: '{self.type} failed with errors: {self.message}"
     
