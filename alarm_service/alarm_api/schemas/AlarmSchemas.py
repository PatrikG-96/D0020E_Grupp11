from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime

class SubscribedAlarmsSchema(Schema):
    """ /alarm/active/subscribed GET
    
    Parameters:
     - user_id
    
    """
    
    userID = fields.Int(required = True)
    
class SubscribeSchema(Schema):
    
    userID = fields.Int(required = True)
    monitorID = fields.Int(required = True)
    
class AlarmReponseSchema(Schema):
    """ /alarm/active/respond POST

    Parameters:
     - alarmID
     - client_id
     - response_code: 0 for read, 1 for solved
     - timestamp
    """
    
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
    