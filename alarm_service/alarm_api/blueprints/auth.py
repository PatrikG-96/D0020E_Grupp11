from http.client import BAD_REQUEST
from flask import Blueprint, make_response, request, jsonify, abort
from schemas.AuthSchemas import *
from datetime import datetime, timedelta
from database.database import setNewUser, getUser
from dotenv import load_dotenv, find_dotenv
import bcrypt
import jwt
import json
import os

auth = Blueprint('auth', __name__)
client_auth_schema = ClientAuthSchema()
client_add_schema = ClientAddSchema()


load_dotenv(find_dotenv())

key = bytes.fromhex(os.getenv("KEY"))

@auth.route("/auth/user/login", methods = ['POST'])
def client_login():
    
    errors = client_auth_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    print(f"Trying to get user with username: {username}")
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


@auth.route("/auth/user/add", methods = ['POST'])
def add_client_user():
    
    print("adding user")
        
    errors = client_auth_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    
    username = request.form.get('username')
    password = request.form.get('password')
        
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        setNewUser(username, hashed_pw, "client")
    except:
        return make_response('Unable to add client user', 403, {'WWW-Authenticate': 'Basic realm: "Registration Failed"'})

    return make_response("Success")
    
