from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime

class RequestAccessSchema(Schema):
    
    user_id = fields.Int(required = True)
    timestamp = fields.String(required =  True)
    
    
    @validates('timestamp')
    def is_timestamp(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            
            raise ValidationError
    
class RevokeAccessSchema(Schema):
    
    user_id = fields.Int(required = True)
    token = fields.String(required = True, validate=Length(64))