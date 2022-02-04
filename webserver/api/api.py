from email import message
from re import M
import bcrypt
import time
from urllib import response
from database import *
from sse import Announcer
from sse import Formatter
from functools import wraps
import secrets
import jwt
from datetime import datetime, timedelta
from flask import Flask, jsonify, make_response, request, Response
from flask_cors import CORS
from pywebpush import webpush, WebPushException
import json


app = Flask(__name__)
cors = CORS(app)

app.config['key'] = secrets.token_bytes(
    32)  # should be stored in file not code
app.config['date_format'] = "%d/%m/%Y - %H:%M:%S"
announcer = Announcer.AlarmAnnouncer(2)

VAPID_PRIVATE_KEY = "2YQXZ1jI7Hywk-Ola-IiojWeZULqZ2ZzX5rwa5UPQc4"
VAPID_PUBLIC_KEY = "BD85L_ud7eQ_gJhg-8GoFXbCE5pHz7_fFrVOtV1W-WrdfTNpgChCA6uQdzJO-67PCJzD-nUH4ThCGauRB9byMdU"
VAPID_CLAIMS = {
    "sub": "mailto:aleekl-8@student.ltu.se"
}


class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        # print(request.headers.get('x-auth-token'))
        token = request.headers.get('x-auth-token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            expireTime = datetime.fromtimestamp(data['exp'])
            print(expireTime)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'Message': 'Signature has expired'}), 403
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated


@app.route('/devices/add')
def add_device():
    data = json.loads(request.data)
    name = data["name"]
    device_id = data["device_id"]


@app.route('/devices/get')
def get_devices():

    return  # all devices


@app.route('/auth/login', methods=['POST'])
def login():

    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]

    user = get_user(username=username)

    if not user:  # Make sure user exists
        return make_response('Login failed', 401)

    if bcrypt.checkpw(password.encode(), user[2].encode()):
        token = jwt.encode(
            {
                'user': username,
                'exp': (datetime.utcnow() + timedelta(seconds=60))
            },
            app.config['key'],
            algorithm="HS256"
        )
        return jsonify({'accessToken': token, 'userID': user.userID})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


@app.route("/auth/signup", methods=['POST'])
def signup():
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]
    print(f"trying to make user: {username}, {password}")
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        print("inbetween")
        newUser(username, hashed_pw)
    except:
        return make_response('Unable to register', 403, {'WWW-Authenticate': 'Basic realm: "Registration Failed"'})

    token = jwt.encode(
        {
            'user': username,
            'exp': (datetime.utcnow() + timedelta(seconds=60))
        },
        app.config['key'],
        algorithm="HS256"
    )
    return jsonify({'accessToken': token})


@app.route("/alarm/listen")
def listen():
    # get all devices that user is subscribed to
    args = request.args
    if not args.get('user_id'):
        return make_response("Fail", 401)
    user = args.get('user_id')

    def stream():
        q = announcer.listen(int(user))
        while True:
            msg = q.get()
            yield msg

    return Response(stream(), mimetype='text/event-stream')


# Idea: For future use, having user id in JWT token encrypted with server secret key,
# it can be verified
@app.route("/alarm/active/<user>")
def get_active_alarm(user):
    args = request.args

    if not args:
        # All active alarms that this user listens to
        return make_response()

    if not args['device_id']:

        return make_response('Invalid arguments', 401)

    # Maybe check for other args?
    # Query for all active alarms for user for specific device
    return make_response()


@app.route("/alarm/history/<device_id>")
def get_alarm_history(device_id):

    args = request.args

    if not args:
        # return entiry history of this device_id
        return make_response()

    if not args['before'] and not args['after']:

        return make_response("Invalid arguments")

    if not args['after']:

        # query for alarms after date
        return make_response()

    if not args['before']:

        # query for alarms before date
        return make_response()

    # query for alarms after date1 but before date2
    return make_response()


@app.route("/alert", methods=['POST'])
def alert():
    print("alert received")
    form = request.form
    user_id = 1
    device = form.get("device_id")
    type = form.get("type")
    msg = Formatter.format_sse(
        str({"device_id": device, "type": type}).replace('\'', '"'))
    announcer.announce_alarm([user_id], msg)
    return make_response("Yo", 201)


@app.route("/subscription", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        if(request.args.get("userID") is not None):
            userID = request.args.get("userID")
            endpoint = getSubscription(userID)
            return Response(response=json.dumps({"endpoint": endpoint}),
                            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
                        headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = json.loads(request.data)["sub"]
    if("endpoint" not in subscription_token):
        return make_response("Subscripion must have an endpoint", 400)

    userID = json.loads(request.data)["userID"]
    successful = storeSubscription(subscription_token, userID)
    if(successful):
        return Response(json.dumps(subscription_token), status=201, mimetype="application/json")


@app.route("/push_alarm", methods=["GET", "POST"])
def push_alarm():
    subscriptions = getAllSubscriptions()

    for sub in subscriptions:
        message_body = json.dumps(
            {"title": "New alarm!", "alarm-type": "fall-detected"})
        try:
            webpush(
                subscription_info=json.loads(sub.endpoint),
                data=message_body,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as ex:
            print(ex.response.status_code)
            if(ex.response.status_code == 410 or ex.response.status_code == 404):
                print(repr(ex))
                deleteSubscription(sub.endpoint)
    return "Alarm notifications sent!"
