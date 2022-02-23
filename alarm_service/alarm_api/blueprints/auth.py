from http.client import BAD_REQUEST
from flask import Blueprint, make_response, request, jsonify, abort
from schemas.AuthSchemas import *
from datetime import datetime, timedelta
from database.database import addClient, getClientUser, setNewUser, getClients
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

@auth.route("/auth/client/login", methods = ['POST'])
def client_login():
    
    errors = client_auth_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    client_id = request.form.get('client_id')
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = getClientUser(client_id, username)
    
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


@auth.route("/auth/client/user/add", methods = ['POST'])
def add_client_user():
    
    errors = client_auth_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.form.get('client_id')
    username = request.form.get('username')
    password = request.form.get('password')
        
    try:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(14))
        setNewUser(client_id, username, hashed_pw)
    except:
        return make_response('Unable to add client user', 403, {'WWW-Authenticate': 'Basic realm: "Registration Failed"'})

    return make_response("Success")
    
@auth.route("/auth/client/add", methods = ['POST'])
def add_client():
    print("asd")
    errors = client_add_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.form.get('client_id')    
    
    print(getClients())
    
    try:
        print(f"here: {client_id}")
        print(f"here: {int(client_id)}")
        addClient(int(client_id))
        return make_response('Success')
    except Exception as e:
        print(e)
        return make_response('Failed at adding client', 403)