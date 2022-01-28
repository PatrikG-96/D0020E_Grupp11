import re
from .MessageTypes import MessageTypes
from .ProtocolException import ProtocolException

class Header:
    """Class representing a header in the Alarm Protocol v1.0

    Attributes
    ----------
    field_names : list
        Class variable, list of header field names

    option_fields : list
        Class variable, list of valid option fields

    version : str
        header version string for instance

    type : MessageType
        header message type 

    options : dict
        dictionary containing all header option fields
    
    Methods
    -------
    setVersion(version)
        Set header version string

    setType(type)
        Set header type to matching MessageType 

    setOptions(options)
        Set header option dictionary

    getVersion()
        Returns the header version string

    getType()
        Returns the header MessageType

    getOptions()
        Returns the header options dictionary

    fromDict(params)
        Creates a Header object using fields from params dictionary
    """

    __version_format = "AP[0-9].[0-9]"
    field_names = ['version', 'type', 'options']
    option_fields = [] # temporary

    def __init__(self):
        self.version = None
        self.type = None
        self.options = {}

    def setVersion(self, version : str):
        """Set the header version.
        
        Parameters
        ----------
        version : string
            The header version string. Follows the format "APx.y" where x and y are integers between 0-9
        
        Raises
        ------
        ProtocolException
            If version string doesn't pass a regex test for valid format
        """
        match = re.match(self.__version_format, version)

        if not (match):
            raise ProtocolException("Header version string does not match format: " + self.version_format)

        self.version = version

    def setType(self, type : int):
        """Set the header message type.
        
        Parameters
        ----------
        type : int
            The integer representing a message type, see MessageTypes enum
        
        Raises
        ------
        ProtocolException
            If type is not a valid type
        """
        if not MessageTypes.has_key(type):
            raise ProtocolException("Unknown message type in Header: ", type)

        self.type = MessageTypes[type]

    def setOptions(self, options : dict):
        """Set the header options.
        
        Parameters
        ----------
        options : dictionary
            A dictionary of option fields.
        
        Raises
        ------
        ProtocolException
            If any fields in option dictionary don't exist in Header.option_fields
        """
        if all(key in  self.option_fields for key in options):
            raise ProtocolException("Unknown option field found.")
     
        self.options = options

    def getVersion(self):
        """Return the header version string.
        
        Returns
        -------
        version
            The header version string of this header object
        """
        return self.version

    def getType(self):
        """Return the header type enumeration.
        
        Returns
        -------
        type
            The header type, see MessageTypes
        """
        return self.type
    
    def getOptions(self):
        """Return the header option dictionary.
        
        Returns
        -------
        options
            The options dictionary of the header object
        """
        return self.options

    @staticmethod
    def __isDictValid(params: dict) -> bool:
        """Checks if dictionary is valid as a parameter dictionary for a header object. 
        
        Field value format is enforced in the setter methods. this method only makes sure the fields exist.
        
        Parameters
        ----------
        params : dict
            Dictionary containing fields for a Alarm Protocol header, following the format
            {field1:value1, field2:value2} etc

        Returns
        -------
        bool
            True if all required fields are found as keys in the dictionary, False otherwise 
        """
        if all(key in params for key in Header.field_names):
            return True

        return False

    @staticmethod
    def fromDict(params_map):
        """Creates a header object using the input parameter dictionary.
        
        Parameters
        ----------
        params_map : dict
            Dictionary containing fields for a Alarm Protocol header, following the format
            {field1:value1, field2:value2} etc

        Returns
        -------
        header : Header 
            A Header object with fields set according to input dictionary

        Raises
        ------
        ProtocolException
            If dictionary fields don't match Header.field_names, or if any of the fields don't pass their respective
            format tests
        """
        if not Header.__isDictValid(params_map):
            raise ProtocolException("Input dictionary does not match required fields.")

        header = Header()
        header.setVersion(params_map['version'])
        header.setType(params_map['type'])
        header.setOptions(params_map['options'])
        return header

    def __str__(self):
        options = ', '.join([f'{key}:{value}' for key, value in self.options.items()])
        return f'{self.version}/{str(self.type).split(".")[1]}/options[' + options + ']'


