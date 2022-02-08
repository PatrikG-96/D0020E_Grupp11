from flask import Blueprint, blueprints
import json
from flask import request, make_response, jsonify
from database.database import *
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

key = bytes.fromhex(os.getenv("SECRET_KEY"))

auth_routes = Blueprint("auth_routes", __name__)

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
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]
    
    user = getUser(username)
    
    if not user: # Make sure user exists
        return make_response('Login failed', 401)

    if bcrypt.checkpw(password.encode(), user[2].encode()):
        token = jwt.encode(
            {

                'user': user[0],
                'exp': str(datetime.utcnow() + timedelta(minutes=60))

            }, 
            key,
            algorithm="HS256"
        )
        return jsonify({'accessToken': token, "userID":user[0]})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})


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
    data = json.loads(request.data)
    username = data["username"]
    password = data["password"]
    
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        setNewUser(username, hashed_pw)
    except:
        return make_response('Unable to register', 403, {'WWW-Authenticate': 'Basic realm: "Registration Failed"'})

    #return redirect(url_for('login'), code=307)
    return make_response("Success")

