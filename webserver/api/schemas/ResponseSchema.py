from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime
import json


class ResponseSchema(Schema):
    
    alarmID = fields.Int(required = True)
    userID = fields.Int(required = True)
    responseCode = fields.Int(required = True)
    timestamp = fields.String(require = True)
    
    @validates('timestamp')
    def is_timestamp(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            
            raise ValidationError
    
response_schema = ResponseSchema()