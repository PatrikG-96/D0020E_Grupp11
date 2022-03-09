from parse import parse_JSON
from marshmallow import Schema, fields, validates, ValidationError, validate, INCLUDE
from marshmallow.validate import Length, Range
import json
from datetime import datetime
from schemas import alarm_notification_schema
from twisted.internet.defer import Deferred

msg = {"type" : "AlarmNotification", "monitor_id" : 1, "alarm_id" : 1, "timestamp" : "2022/02/16 21:26:43", "sensor_id" : 2,
       "sensor_info" : "widefindXXXX", "alarm_type" : "fall", "info" : {}}

msg1 = {"type" : "SensorAlert", "sensor_id" : "1", "sensor_name" : "asd", "timestamp" : "2020-02-22 03:19:43", 'alarm_type' : "fall_confirmed",
        "params" : {'coords' : "(1,2,3)"}}


res = parse_JSON(msg1)
print(type(res))