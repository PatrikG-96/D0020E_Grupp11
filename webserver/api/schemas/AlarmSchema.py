from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime
import json

class AlarmSchema(Schema):
    
    type = fields.String(required = True)
    sensor_id = fields.String(required = True)
    sensor_info = fields.String(required = True)
    alarm_type = fields.String(required = True)
    monitor_id = fields.Int(required = True)
    timestamp = fields.String(required = True)
    alarm_id = fields.Int(required = True)
    info = fields.Dict(required = True)
    
    
    @validates('timestamp')
    def is_timestamp(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            
            raise ValidationError("Invalid timestamp")
    
alarm_schema = AlarmSchema()
