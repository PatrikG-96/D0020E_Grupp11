from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime
import json


class SubscribeSchema(Schema):
    
    userID = fields.Int(required = True)
    monitorID = fields.Int(required = True)
    
subscribe_schema = SubscribeSchema()