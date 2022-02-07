from flask import Blueprint
from database.database import *

device_routes = Blueprint('device_rotes', __name__)

@device_routes.route("/devices/all")
def get_all_devices():

    devices = getDevices()
    result = {}
    for device in devices:
        result[device[0]] = device[1]
        
    return result
