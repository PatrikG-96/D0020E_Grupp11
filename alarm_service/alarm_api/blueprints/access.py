from http.client import BAD_REQUEST
from flask import Blueprint, request, abort
from schemas.AccessSchemas import RequestAccessSchema
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

key = bytes.fromhex(os.getenv("KEY"))

request_access_schema = RequestAccessSchema()

access = Blueprint('access', __name__)


@access.route("/server/access/request")
#@.....
def request_server_access():
    
    errors = request_access_schema.validate(request.form)
    
    if errors:
        abort(BAD_REQUEST, str(errors))
        
    client_id = request.form.get('client_id')
    timestamp = request.form.get('timestamp')
    
    