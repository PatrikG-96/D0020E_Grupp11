from flask import Blueprint, current_app
import requests
from dotenv import load_dotenv, find_dotenv
import os
from routes.decorators.auth_decorators import token_required
from database.database import setNewMonitor

load_dotenv(find_dotenv())

api_url = os.getenv("ALARM_API")
device_routes = Blueprint('device_rotes', __name__)

#Tested
@device_routes.route("/monitor/all")
@token_required
def get_all_devices():

    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url + "/monitor/all", headers = header)
    
    for id, name in result.json().items():
        try:
            setNewMonitor(id, name)
        except Exception as e:
            print(f"Monitor {id} already exists")
            continue
        print(f"added new monitor: {id}")
    
    return result.json()
