from database.database import *
from flask import Blueprint, request, Response, make_response
from pywebpush import webpush, WebPushException

webpush_routes = Blueprint('webpush_routes', __name__)

VAPID_PRIVATE_KEY = "2YQXZ1jI7Hywk-Ola-IiojWeZULqZ2ZzX5rwa5UPQc4"
VAPID_PUBLIC_KEY = "BD85L_ud7eQ_gJhg-8GoFXbCE5pHz7_fFrVOtV1W-WrdfTNpgChCA6uQdzJO-67PCJzD-nUH4ThCGauRB9byMdU"
VAPID_CLAIMS = {
    "sub": "mailto:aleekl-8@student.ltu.se"
}

@webpush_routes.route("/subscription", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        if(request.args.get("userID") is not None):
            userID = request.args.get("userID")
            endpoint = getSubscription(userID)
            print(endpoint)
            return Response(response=json.dumps({"endpoint": endpoint}),
                            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
                        headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = json.loads(request.data)["sub"]
    if("endpoint" not in subscription_token):
        return make_response("Subscripion must have an endpoint", 400)

    userID = json.loads(request.data)["userID"]
    print(f"here: {userID}")
    successful = storeSubscription(subscription_token, userID)
    if(successful):
        return Response(json.dumps(subscription_token), status=201, mimetype="application/json")


@webpush_routes.route("/push_alarm", methods=["GET", "POST"])
def push_alarm():
    subscriptions = getAllSubscriptions()

    for sub in subscriptions:
        message_body = json.dumps(
            {"title": "New alarm!", "alarm-type": "fall-detected"})
        print(message_body)
        
        try:
            print("pushing")
            webpush(
                subscription_info=json.loads(sub.endpoint),
                data=message_body,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print("pushed")
        except WebPushException as ex:
            print(ex.response.status_code)
            if(ex.response.status_code == 410 or ex.response.status_code == 404):
                print(repr(ex))
                deleteSubscription(sub.endpoint)
    return "Alarm notifications sent!"
