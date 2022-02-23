from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class ClientAuthSchema(Schema):
    
    """ /auth/client/login - POST   
    
    Parameters:
     - client id
     - username
     - password
    """
    
    client_id = fields.Int(required = True)
    username = fields.Str(required = True, validate=Length(max=128))
    password = fields.Str(required = True)
    
class ClientAddSchema(Schema):
    
    """ /auth/client/add - POST   
    
    Parameters:
     - client id
    """
    
    client_id = fields.Int(required = True)
    
