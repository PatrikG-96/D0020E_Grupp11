from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime
from __main__ import app

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        #print(request.headers.get('x-auth-token'))
        token = request.headers.get('x-auth-token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            expireTime = datetime.fromtimestamp(data['expires'])
            print(expireTime)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'Message': 'Signature has expired'}), 403
        except jwt.exceptions.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)    
    return decorated
