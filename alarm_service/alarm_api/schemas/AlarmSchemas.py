from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime

class SubscribedAlarmsSchema(Schema):
    """ /alarm/active/subscribed GET
    
    Parameters:
     - client_id
    
    """
    
    client_id = fields.Int(required = True)
    
class SubscribeSchema(Schema):
    
    client_id = fields.Int(required = True)
    monitor_id = fields.Int(required = True)
    
class AlarmReponseSchema(Schema):
    """ /alarm/active/respond POST

    Parameters:
     - alarm_id
     - client_id
     - response_code
     - timestamp
    """
    
    alarm_id = fields.Int(required = True)
    client_id = fields.Int(required = True)
    response_code = fields.Int(required = True)
    timestamp = fields.DateTime(require = True)
    
    @validates('timestamp')
    def is_timestamp(value):
        
        try:
            datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            raise ValidationError
            