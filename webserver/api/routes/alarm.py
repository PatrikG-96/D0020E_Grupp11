from database.database import *
from flask import Blueprint, request, make_response

alarm_routes = Blueprint('alarm_routes', __name__)

@alarm_routes.route("/alarm/response")
def alarm_response():
    #data = json.loads(request.data)
    #alarmID = data['alarmID']
    #userID = data['userID']
    #read = data['read']
    #resolved = data['resovled']
    
    args = request.args
    
    alarmID = args.get('alarm_id')
    timestamp = args.get('timestamp')
    userID = args.get('user_id')
    read = args.get('read')
    resolved = args.get('resolved')
    
    if read=='1':
        readAlarm(alarmID, userID, timestamp)
    if resolved=='1':
        resolveAlarm(alarmID, userID, timestamp)
        
    return make_response("success", 201)
    
    
@alarm_routes.route("/alarm/active/all")
#@token_required
def get_active_alarm():

    alarms = getAllAlarmNotRead()
    print(alarms)
    result = {"length" : len(alarms)}
    i = 0
    for alarm in alarms:
        result[str(i)] = {'alarmID' : alarm[0], 'type' : alarm[1], 'deviceID' : alarm[2], 'read' : alarm[3], 'resolved': alarm[4]}
        i+=1
    return result


@alarm_routes.route("/alarm/active/subscribed")
#@token_required
def get_active_subscribed_alarms():
    
    uid = request.args.get('user_id')
    
    alarms = getUserActiveAlarms(uid)
    result = {'length' : len(alarms)}
    i = 0
    for alarm in alarms:
        result[str(i)] = {'alarmID' : alarm[0], 'type' : alarm[1], 'deviceID' : alarm[2], 'read' : alarm[3], 'resolved' : alarm[4]}
        i+=1
        
    return result

@alarm_routes.route("/alarm/subscribe")
#@token_required
def subscribe_to_alarm():
    
    #token = request.headers.get('x-auth-token')
    #data = jwt.decode(token, app.config['KEY'])
    #uid = data['user']
    uid = 10
    #data = json.loads(request.data)
    data = request.args
    device_id = data['device_id']    
    
    if setNewSubscription(uid, device_id):
        return make_response("success", 201)
    return make_response("failed", 401)
    

@alarm_routes.route("/alarm/all")
def get_all_alarms():
    
    alarms = getAllAlarms()
    result = {"length" : len(alarms)}
    i = 0
    for alarm in alarms:
        result[str(i)] = {'alarmID' : alarm[0], 'type' : alarm[1], 'deviceID' : alarm[2], 'read' : alarm[3], 'resolved': alarm[4]}
        i+=1
        
    return result
