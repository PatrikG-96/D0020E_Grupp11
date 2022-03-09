from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range
from datetime import datetime
import json


class ConnectedSchema(Schema):
    
    userID = fields.Int(required = True)
    jwt = fields.String(required = True)
    
connected_schema = ConnectedSchema()