
from email import message
from marshmallow import Schema, fields, validates, ValidationError, INCLUDE
from marshmallow.validate import Length, Range
from datetime import datetime
from protocol.messages import response_types
#from messages import response_types



class MessageSchema(Schema):
    class Meta:
        unknown = INCLUDE
    
    type = fields.String(required = True)

class SensorAlertSchema(MessageSchema):
    sensor_id = fields.Int(required = True)
    sensor_name = fields.String(required = True)
    alarm_type = fields.String(required = True)
    timestamp = fields.String(required = True)
    params = fields.Dict(required = True)
    
    @validates('timestamp')
    def is_timestamp(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            
            raise ValidationError
    

class SensorAlertResponseSchema(MessageSchema):
    
    received = fields.Bool(required = True)    
    
class RequireTokenSchema(MessageSchema): pass

class TokenResponseSchema(MessageSchema):
    
    token = fields.String(required = True)
    client_id = fields.Int(required = True)
    
class TokenAuthResultSchema(MessageSchema):
    
    success = fields.Bool(required = True)

class AlarmSchema(MessageSchema):
    
    timestamp = fields.String(required = True)
    alarm_id = fields.Int(required = True)
    info = fields.Dict(required = True)
    
    @validates('timestamp')
    def is_timestamp(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            
            raise ValidationError
    

class AlarmNotificationSchema(AlarmSchema):
    
    sensor_id = fields.Int(required = True)
    sensor_info = fields.String(required = True)
    alarm_type = fields.String(required = True)
    monitor_id = fields.Int(required = True)
    
class AlarmResponseSchema(AlarmSchema):
    
    response_type = fields.String(required = True)
    client_id = fields.Int(required = True)
    
    @validates('response_type')
    def response_validate(self, response):
        
        if response not in response_types:
            raise ValidationError
        
class AlarmResponseConfirmationSchema(AlarmResponseSchema):
    
    success = fields.Bool(required = True)
        
require_token_schema = RequireTokenSchema()
token_response_schema = TokenResponseSchema()
token_result_schema = TokenAuthResultSchema()
alarm_notification_schema = AlarmNotificationSchema()
alarm_response_schema = AlarmResponseSchema()
alarm_response_confirmation_schema = AlarmResponseConfirmationSchema()
sensor_alert_schema = SensorAlertSchema()
sensor_alert_response_schema = SensorAlertResponseSchema()
message_schema = MessageSchema()