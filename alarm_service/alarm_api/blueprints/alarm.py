
from http.client import BAD_REQUEST
from pydoc import resolve
from flask import Blueprint, make_response, request, abort
from database.database import *
from schemas.AlarmSchemas import SubscribedAlarmsSchema, AlarmReponseSchema, SubscribeSchema
from blueprints.decorators.auth_decorator import token_required

alarm = Blueprint('alarm', __name__)
subscribed_alarms_schema = SubscribedAlarmsSchema()
alarm_response_schema = AlarmReponseSchema()
subcribe_schema = SubscribeSchema()

__READ = 0
__SOLVED = 1

def __format_alarms(alarm_list):
    result = {'length' : len(alarm_list)}
    
    i = 0
    for alarm in alarm_list:
        
        result[str(i)] = {'alarmID' : alarm.alarmID, 'type' : alarm.alarmtype.nameType, 'monitorID' : alarm.monitorID, 
                          'read' : alarm.read, 'resolved': alarm.resolved, "timestamp" : alarm.timestamp}
        i+=1
    
    return result

@alarm.route('/alarm/active/all', methods = ['GET'])
#@token_required
def get_all_active_alarms():
    """ API endpoint for retreiving all active alarms
    """
    
    alarms = getAllAlarmNotRead()
    
    return __format_alarms(alarms)






@alarm.route('/alarm/active/subscribed', methods = ['GET'])
@token_required
def get_subscribed_active_alarms():
    """ API endpoint for getting client subscribed active alarms
    """
    errors = subscribed_alarms_schema.validate(request.args)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    user_id = request.args.get('userID')
        
    alarms = getUserActiveAlarms(user_id)
    
    return __format_alarms(alarms)

@alarm.route("/alarm/all")
@token_required
def get_all_alarms():
    """ API endpoint for retreiving all alarms, both active and resolved
    """
    #INCLUDE optional filtering
    
    alarms = getAllAlarms()
    
    return __format_alarms(alarms)

@alarm.route("/alarm/subscribe")
@token_required
def subscribe_to_alarm():
    """ API endpoint for adding a subcription for the specified client to the specified monitor
    """
    errors = subcribe_schema.validate(request.args)
    
    if errors:
        print(str(errors))
        abort(BAD_REQUEST, str(errors))
    
    
    client_id = request.args.get('userID')
    monitor_id = request.args.get('monitorID')
    
    if setNewSubscription(client_id, monitor_id):
        return {'status' : 'added'}
    else:
        return {'status' : 'existed'}
    
@alarm.route("/alarm/unsubscribe", methods = ['POST'])
@token_required
def unsubscribe_to_alarm():
    
    errors = subcribe_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.form.get('client_id')
    monitor_id = request.form.get('monitor_id')
    
    try:
        deleteSubscription(int(client_id), int(monitor_id))
        return {"status" : "success"}
    except:
        return {"status" : "failed"}
    
    
@alarm.route("/alarm/active/respond", methods = ['POST'])
@token_required
def respond_to_alarm():
    """ API endpoint for responding to an active alarm
    """
    errors = alarm_response_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    code = int(request.form.get("responseCode"))
    alarmID = request.form.get("alarmID")
    timestamp = request.form.get("timestamp")
    userID = int(request.form.get("userID"))
    
    try :
        if code == __READ:
            print("should read alarm")
            readAlarm(int(alarmID), userID, timestamp)
        
        elif code == __SOLVED:
            print("should solve alarm")
            resolveAlarm(int(alarmID), userID, timestamp)
            
    except Exception as e:
        print(str(e))
        return {"status" : "failed"}
        
    return {'status' : 'success'}
    
