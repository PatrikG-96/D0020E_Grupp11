from http.client import BAD_REQUEST
from database.database import *
from flask import Blueprint, request, make_response, Response, abort, current_app
from sse.Announcer import AlarmAnnouncer
from sse import Formatter
from routes.webpush import push_alarm
from schemas.AlarmSchema import alarm_schema
from routes.decorators.auth_decorators import token_required

"""
This module contains routes to do with SSE.

Attributes
----------
sse_routes : Blueprint
    Blueprint containing all routes in this module. Use this to register the routes.
"""

sse_routes = Blueprint('sse_routes', __name__)

announcer = AlarmAnnouncer(5)

@sse_routes.route("/alarm/listen")
@token_required
def listen():
    """Endpoint for listening to SSE
    
    URL arguments
    -------------
    user_id : int
        unique ID of the user
        
    Returns
    -------
    A connection is established. Technically all SSE messages are returned through
    this stream.
    """
    
    if not current_app.config['LISTENER_CONNECTED']:
        return make_response({"status" : "API listener not connected"}, 503)
    
    
    args = request.args
    if not args.get('user_id'):
        return make_response("Fail", 401)
    user = args.get('user_id')

    def stream():
        q = announcer.listen(int(user))
        while True:
            msg = q.get()
            print("sending message to client")
            yield msg
    
    return Response(stream(), mimetype='text/event-stream')

#Is triggered by api_listener    
@sse_routes.route("/alert", methods=['POST'])
def alert():
    """Endpoint for triggering alarm alerts
    
    Methods: POST
    
    Form
    ----
    All fields found in an AlarmNotification message, see Protocol
    
    Returns
    -------
    A JSON indicating whether or not SSE succeeded or not
    """
    form = json.loads(request.data.decode())
    
    errors = alarm_schema.validate(form)
    
    if errors:
        abort(BAD_REQUEST, errors)
    
    
    monitor = form["monitor_id"]
    type = form["alarm_type"]
    timestamp = form["timestamp"]
    info = form['info']
    sensor_id = form['sensor_id']
    sensor_info = form['sensor_info']
    alarm_id = form['alarm_id']
    
    
    if type == "fall_confirmed":
        form["coords"] = info['coords']
        del form['info']
    
    
    subs = getSubscribers_m(monitor)
    uids_list = []
    for sub in subs:
        uids_list.append(sub.userID)
    
    # This triggers web push notifications, uncomment to test, not 100%
    # functioning at the moment    
    #push_alarm(uids_list, type)
    
    format_msg = Formatter.format_sse(json.dumps(form))
    announcer.announce_alarm(uids_list, format_msg)
    return {"success" : "Yes"}
