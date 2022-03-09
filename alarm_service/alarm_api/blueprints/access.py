from http.client import BAD_REQUEST
from random import randbytes
from flask import Blueprint, request, abort
from schemas.AccessSchemas import RequestAccessSchema, RevokeAccessSchema
from dotenv import load_dotenv, find_dotenv
from database.database import addServerAccessToken, deleteServerAccess
import os
from blueprints.decorators.auth_decorator import token_required
from Crypto.Hash import SHA256

load_dotenv()

key = bytes.fromhex(os.getenv("KEY"))
server_ip = os.getenv('SERVER_IP')
server_port = os.getenv('SERVER_PORT')


request_access_schema = RequestAccessSchema()
revoke_access_schema = RevokeAccessSchema()

access = Blueprint('access', __name__)


def generate_token(size):
    # Could have a better implementation
    return randbytes(size)

@access.route("/server/access/request", methods=['POST'])
@token_required
def request_server_access():
    
    errors = request_access_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    user_id = request.form.get('user_id')
    timestamp = request.form.get('timestamp')
    
    
    digest = SHA256.new(data=generate_token(32))
    token = digest.hexdigest()
     
    #Request was validated, JWT was validated, client should get server access
    try:
        access = addServerAccessToken(int(user_id), token, timestamp)
    except Exception as e:
        return {"error" : "Access was granted, but generating token failed with error: " + str(e)}
    
    
    return {"token" : access.token, "ip" : server_ip, "port" : server_port}
    
@access.route("/server/access/revoke", methods = ['POST'])
#@...
def revoke_server_access():
    
    errors = revoke_access_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    user_id = request.form.get('user_id')
    token = request.form.get('token')
    
    try:
        deleteServerAccess(int(user_id), token)
    except Exception as e:
        return {"error" : "Could not delete access token"}
    
    
    return {"success" : "true"}
    
    
    
    