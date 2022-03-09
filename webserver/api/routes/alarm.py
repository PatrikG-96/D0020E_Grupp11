from http.client import BAD_REQUEST
from database.database import *
from flask import Blueprint, request, make_response, abort, current_app
from routes.webpush import push_alarm
from schemas.SubscribeSchema import subscribe_schema
from schemas.ResponseSchema import response_schema
from routes.decorators.auth_decorators import token_required
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

api_url = os.getenv("ALARM_API")

alarm_routes = Blueprint('alarm_routes', __name__)

#Tested
@alarm_routes.route("/alarm/response", methods = ['POST'])
@token_required
def alarm_response():
    
    if not current_app.config['LISTENER_CONNECTED']:
        return make_response({"status" : "API listener not connected"}, 503)
    
    errors = response_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    msg = request.form.to_dict()
    msg['userID'] = current_app.config['CLIENT_ID']
    
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.post(api_url+"/alarm/active/respond", msg, headers = header)    
    
    return result.json()
    
#Tested 
@alarm_routes.route("/alarm/active/all")
@token_required
def get_active_alarm():

    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+"/alarm/active/all", headers = header)

    return result.json() 

#Tested, just dumb implementation
@alarm_routes.route("/alarm/subscribed")
@token_required
def get_active_subscribed_alarms():
    
    if not current_app.config['LISTENER_CONNECTED']:
        return make_response({"status" : "API listener not connected"}, 503)
    
    
    uid = request.args.get('userID')
    
    subs = getUserDeviceSubscriptions(int(uid))
    
    if len(subs) == 0:
        return {"status" : "no subscriptions"}
    
    monitor_ids = []
    for sub in subs:
        monitor_ids.append(sub.monitorID)
    
    print("montor ids:" + str(monitor_ids))
    
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+f"/alarm/active/subscribed?userID={current_app.config['CLIENT_ID']}", headers = header)
    
    
    res = {}
    i = 0
    for key, value in result.json().items():
        
        if key == "length":
            continue
        if int(value['monitorID']) in monitor_ids:
            res[str(i)] = value
        i+=1
      
    return res


#Tested
@alarm_routes.route("/alarm/subscribe", methods = ['POST'])
@token_required
def subscribe_to_alarm():
    
    if not current_app.config['LISTENER_CONNECTED']:
        return make_response({"status" : "API listener not connected"}, 503)
    
    
    errors = subscribe_schema.validate(request.args)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    
    monitorID = request.args.get('monitorID')
    userID = request.args.get('userID')
    
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+f"/alarm/subscribe?userID={current_app.config['CLIENT_ID']}&monitorID={monitorID}", headers = header)
    
    # If the result isn't json serializable, the request failed
    try:
        result.json()
    except:
        abort(BAD_REQUEST, "Subscription failed")
    
    
    
    if setNewSubscription(userID, monitorID):
        return {"status" : "success"}
    return {"status" : "failed"}
    
#Tested
@alarm_routes.route("/alarm/all")
@token_required
def get_all_alarms():
    
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+"/alarm/all", headers = header)
    
    return result.json()
