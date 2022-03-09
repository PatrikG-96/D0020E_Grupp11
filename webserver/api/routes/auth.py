from http.client import BAD_REQUEST
from flask import Blueprint, blueprints
import json
from flask import request, make_response, jsonify, abort, current_app
from database.database import *
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
from schemas.ConnectedSchema import connected_schema
import os

load_dotenv(find_dotenv())

key = bytes.fromhex(os.getenv("SECRET_KEY"))
currentSignupCode = "D0020E_GRUPP11"


auth_routes = Blueprint("auth_routes", __name__)

#Tested
@auth_routes.route('/auth/login', methods=['POST'])
def login():
    """
    Verifies user credentials and returns a JWT for further verification
    Loads data from request.data and converts it to JSON format. Expects fields 'username' and 'password'

    Returns
    -------
        If login succeeds, JSON with the 'accessToken' tag which contains a JWT. JWT contains field 'user_id' and 'expires'
        If login failes, HTTP header response code 403
    """
    data = request.form
    username = data["username"]
    password = data["password"]
    
    user = getUser(username)
    
    if not user: # Make sure user exists
        return make_response('Login failed', 401)

    if bcrypt.checkpw(password.encode(), user.password.encode()):
        token = jwt.encode(
            {
                'user': user.userID,
                'expires': (datetime.utcnow() + timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")

            }, 
            key,
            algorithm="HS256"
        )
        return jsonify({'accessToken': token, "userID":user.userID})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

#Tested
@auth_routes.route("/auth/signup", methods=['POST'])
def signup():
    """
    Registers a new user
    Loads data from request.data and converts it to JSON format. Expects fields 'username' and 'password'.

    Returns
    -------
        If register succeeds, JSON with the 'accessToken' tag which contains a JWT. JWT contains field 'user_id' and 'expires'
        If register failes, HTTP header response code 403
    """
    data = request.form
    username = data["username"]
    password = data["password"]
    signupCode = data["signupCode"]

    if(currentSignupCode != signupCode):
        return make_response('Not a valid signup code', 403)
    
    
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        setNewUser(username, hashed_pw, "user")
    except:
        return make_response('Unable to register', 403, {'WWW-Authenticate': 'Basic realm: "Registration Failed"'})

    return {"status" : "success"}


@auth_routes.route("/auth/client/connected", methods = ['POST'])
def connect_as_client():
    
    print("Connected!")
    
    errors = connected_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    
    current_app.config['LISTENER_CONNECTED'] = True
    current_app.config['CLIENT_ID'] = request.form.get('userID')
    current_app.config['JWT'] = request.form.get('jwt')
    
    
    return {"status" : "success"}
    