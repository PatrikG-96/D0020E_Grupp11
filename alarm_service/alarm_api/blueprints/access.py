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

"""
This module contains routes to do with requesting and revoking access to the alarm server.

Attributes
----------
access : Blueprint
    Blueprint containing all routes in this module. Use this to register the routes.
"""

access = Blueprint('access', __name__)


def generate_token(size):
    # Could have a better implementation
    return randbytes(size)

@access.route("/server/access/request", methods=['POST'])
@token_required
def request_server_access():
    """
    Endpoint for requesting server access

    Methods: POST
    
    Post form
    ---------
    user_id : int
        unique user ID
    timestamp : string
        timestamp in string form
        
    Returns
    -------
    JSON data with a server access token, the servers IP and port, or an error tag if failed
    """
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
        # For some reason the token could not be added, this should be improved
        return {"error" : "Access was granted, but generating token failed with error: " + str(e)}
    
    
    return {"token" : access.token, "ip" : server_ip, "port" : server_port}
    
@access.route("/server/access/revoke", methods = ['POST'])
@token_required
def revoke_server_access():
    """
    Endpoint for revoking access to the server
    
    Methods: POST
    
    Post form
    ---------
    user_id : int
        unique user ID
    token : string
        access token to revoke
        
    Returns
    -------
    JSON data with a "success" tag, or an "error" tag if failed
    """
    
    errors = revoke_access_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
    
    user_id = request.form.get('user_id')
    token = request.form.get('token')
    
    try:
        deleteServerAccess(int(user_id), token)
    except Exception as e:
        # More specific error management might be good here
        return {"error" : "Could not delete access token"}
    
    return {"success" : "true"}
    
    
    
    