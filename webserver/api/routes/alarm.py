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


"""
This module contains routes to do with requesting alarm data and subscribing to monitors/alarms

Attributes
----------
alarm_routes : Blueprint
    Blueprint containing all routes in this module. Use this to register the routes.
"""
load_dotenv(find_dotenv())

api_url = os.getenv("ALARM_API")

alarm_routes = Blueprint('alarm_routes', __name__)

#Tested
@alarm_routes.route("/alarm/response", methods = ['POST'])
@token_required
def alarm_response():
    """Endpoint for responding to an alarm
    
    Methods : POST
    
    POST form
    ---------
    userID : int
        unique ID for the user
    alarmID : int
        unique ID for the alarm
    timestamp : str
        timestamp in string format
    responseCode : int
        an int coding of the response type
        
    Returns
    -------
    Result of API requeset to alarm API. 
    """
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
@alarm_routes.route("/alarm/active/all", methods = ['GET'])
@token_required
def get_active_alarm():
    """Endpoint for getting all active alarms
    
    Methods : GET
    
    Returns
    -------
    Result of API request to alarm API for all alarms
    """
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+"/alarm/active/all", headers = header)

    return result.json() 

#Tested, just dumb implementation
@alarm_routes.route("/alarm/subscribed", methods = ['GET'])
@token_required
def get_active_subscribed_alarms():
    """Endpoint for getting all active alarms that user is subscribed to

    Methods : GET
    
    URL arguments
    -------------
    userID : int
        unique ID of the user
        
    Returns
    -------
    Result from API request to alarm API containing this users subscribed active alarms
    """
    
    # Dumb implementation - issue of converting subscribers clientside to monitor subscriptions
    # server side
    
    if not current_app.config['LISTENER_CONNECTED']:
        return make_response({"status" : "API listener not connected"}, 503)
    
    
    uid = request.args.get('userID')
    
    # Get all the users subscriptions for this client
    subs = getUserDeviceSubscriptions(int(uid))
    
    if len(subs) == 0:
        return {"status" : "no subscriptions"}
    
    # From the subscriptions, get all the monitors user is subscribed to
    monitor_ids = []
    for sub in subs:
        monitor_ids.append(sub.monitorID)
    
    # Make the API request to alarm API, using this APIs client id. This results in all alarms
    # that any user of this client is subscribed to, very inefficient, needs redesign
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+f"/alarm/active/subscribed?userID={current_app.config['CLIENT_ID']}", headers = header)
    
    # Filter out alarms from the monitors that this specific user is subscribed to within the scope 
    # of this client
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
    """Endpoint for subscribing to a monitor
    
    Methods: POST
    
    URL arguments
    -------------
    userID : int
        unique ID of the user
    monitorID : int
        unique ID of the monitor
        
    Returns
    -------
    Result from API request to alarm API. JSON data that indicates the success or failure of the request
    """
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
    """Endpoint for getting all alarms
    
    Returns
    -------
    Result from API request to alarm API. JSON with all alarms.
    """
    header = {'x-auth-token' : current_app.config['JWT']}
    result = requests.get(api_url+"/alarm/all", headers = header)
    
    return result.json()
