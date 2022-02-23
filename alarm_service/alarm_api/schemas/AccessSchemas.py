from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime

class RequestAccessSchema(Schema):
    
    client_id = fields.Int(required = True)
    timestamp = fields.DateTime(required =  True)
    
    @validates('timestamp')
    def is_timestamp(value):
        
        try:
            datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            raise ValidationError
    
    