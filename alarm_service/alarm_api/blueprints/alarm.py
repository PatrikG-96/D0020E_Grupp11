
from http.client import BAD_REQUEST
from flask import Blueprint, make_response, request, abort
from alarm_service.alarm_api.database.database import deleteSubcription
from database.database import getAllAlarmNotRead, getUserActiveAlarms, getAllAlarms, setNewSubscription, deleteSubcription
from schemas.AlarmSchemas import SubscribedAlarmsSchema, AlarmReponseSchema, SubscribeSchema

alarm = Blueprint('alarm', __name__)
subscribed_alarms_schema = SubscribedAlarmsSchema()
alarm_response_schema = AlarmReponseSchema()
subcribe_schema = SubscribeSchema()

def __format_alarms(alarm_list):
    result = {'length' : len(alarm_list)}
    
    i = 0
    for alarm in alarm_list:
        result[str(i)] = {'alarmID' : alarm[0], 'type' : alarm[1], 'deviceID' : alarm[2], 'read' : alarm[3], 'resolved': alarm[4]}
        i+=1
    
    return result

@alarm.route('/alarm/active/all')
#@require client
def get_all_active_alarms():
    """ API endpoint for retreiving all active alarms
    """
    
    alarms = getAllAlarmNotRead()
        
    return __format_alarms(alarms)

@alarm.route('/alarm/active/subscribed')
#@require token
def get_subscribed_active_alarms():
    """ API endpoint for getting client subscribed active alarms
    """
    errors = subscribed_alarms_schema.validate(request.args)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.args.get('client_id')
        
    alarms = getUserActiveAlarms(client_id)
    
    return __format_alarms(alarms)

@alarm.route("/alarm/all")
#.....
def get_all_alarms():
    """ API endpoint for retreiving all alarms, both active and resolved
    """
    #INCLUDE optional filtering
    
    alarms = getAllAlarms()
    
    return __format_alarms(alarms)

@alarm.route("/alarm/subscribe", methods = ['POST'])
#.....
def subscribe_to_alarm():
    """ API endpoint for adding a subcription for the specified client to the specified monitor
    """
    errors = subcribe_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    client_id = request.form.get('client_id')
    monitor_id = request.form.get('monitor_id')
    
    try:
        setNewSubscription(client_id, monitor_id)
        return make_response("Successfully unsubscribed", 200)
    except:
        return make_response("Failed at subscribing", 404)

@alarm.route("/alarm/unsubscribe")
#.....
def unsubscribe_to_alarm():
    
    errors = subcribe_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.form.get('client_id')
    monitor_id = request.form.get('monitor_id')
    
    try:
        deleteSubcription(client_id, monitor_id)
        return make_response("Successfully unsubscribed", 200)
    except:
        return make_response("Failed at subscribing", 404)
    
    
@alarm.route("/alarm/active/respond", methods = ['POST'])
#....
def respond_to_alarm():
    """ API endpoint for responding to an active alarm
    """
    errors = alarm_response_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    return {'success' : 'yes'}
    
