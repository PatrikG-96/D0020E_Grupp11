
from email import message
from marshmallow import Schema, fields, validates, ValidationError, INCLUDE
from marshmallow.validate import Length, Range
from datetime import datetime
from protocol.messages import response_types
#from messages import response_types

"""
This module contains Marshmallow schemas for validating protocol message JSON data.
No instances of these classes need to be created outside this module, the following
attributes already exist:

    require_token_schema : RequireTokenSchema
    token_response_schema : TokenResponseSchema
    token_result_schema : TokenAuthResultSchema
    alarm_notification_schema : AlarmNotificationSchema
    alarm_response_schema : AlarmResponseSchema
    alarm_response_confirmation_schema : AlarmResponseConfirmationSchema
    sensor_alert_schema : SensorAlertSchema
    sensor_alert_response_schema : SensorAlertResponseSchema
    message_schema : MessageSchema
    
If validation is required, use these. Their function should be obvious due to
the naming convention.
"""

class MessageSchema(Schema):
    """
    Schema for validating a generic Message
    """
    class Meta:
        unknown = INCLUDE
    
    type = fields.String(required = True)

class SensorAlertSchema(MessageSchema):
    
    """
    Schema for validating a SensorAlert message
    """
    
    sensor_id = fields.String(required = True)
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
    
    """
    Schema for validating a SensorAlertResponse message
    """
    
    received = fields.Bool(required = True)    
    
class RequireTokenSchema(MessageSchema): 
    """
    Schema for validating a RequireToken message. Technically redundant as the format is identical to a 
    generic message. Exists for completionisms sake and for more clarity in code.
    """
    
    pass

class TokenResponseSchema(MessageSchema):
    
    """
    Schema for validating a TokenResponse message
    """
    
    token = fields.String(required = True)
    username = fields.String(required = True)
    password = fields.String(required = True)
    
class TokenAuthResultSchema(MessageSchema):
    
    """
    Schema for validating a TokenAuthResult message
    """
    
    success = fields.Bool(required = True)

class AlarmSchema(MessageSchema):
    
    """
    Schema for validating a generic Alarm message
    """
    
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
    
    """
    Schema for validating a AlarmNotification message
    """
    
    sensor_id = fields.String(required = True)
    sensor_info = fields.String(required = True)
    alarm_type = fields.String(required = True)
    monitor_id = fields.Int(required = True)
    
class AlarmResponseSchema(AlarmSchema):
    
    """
    Schema for validating a AlarmResponse message
    """
    
    response_type = fields.String(required = True)
    client_id = fields.Int(required = True)
    
    @validates('response_type')
    def response_validate(self, response):
        
        if response not in response_types:
            raise ValidationError
        
class AlarmResponseConfirmationSchema(AlarmResponseSchema):
    
    """
    Schema for validating a AlarmResponseConfirmation message
    """
    
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