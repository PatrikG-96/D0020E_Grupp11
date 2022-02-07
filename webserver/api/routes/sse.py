from database.database import *
from flask import Blueprint, request, make_response, Response
from sse.Announcer import AlarmAnnouncer
from sse import Formatter

sse_routes = Blueprint('sse_routes', __name__)

announcer = AlarmAnnouncer(5)

@sse_routes.route("/alarm/listen")
def listen():
    
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

    
@sse_routes.route("/alert", methods=['POST'])
def alert():
    
    form = request.form  # should be a DB query for all user_ids that subscribe to the device
    device = form.get("device_id")
    type = form.get("type")
    timestamp = form.get("timestamp")
    coords = form.get("coords")
    
    uids = getSubscribers(device)
    uids_list = []
    for uid in uids:
        uids_list.append(uid[0])
    print(uids_list)
    
    msg = Formatter.format_sse(str({"device_id" : device, "type" : type, "timestamp" : timestamp,
                                    "coords" : coords}).replace('\'', '"'))
    announcer.announce_alarm(uids_list, msg)
    return make_response("Yo", 201)
