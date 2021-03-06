from flask import Flask, send_file
import secrets
from flask_cors import CORS
from routes.auth import auth_routes
from routes.alarm import alarm_routes
from routes.device import device_routes
from routes.sse import sse_routes
from routes.webpush import webpush_routes

app = Flask(__name__)
cors = CORS(app)

app.config['LISTENER_CONNECTED'] = False
app.config['CLIENT_ID'] = None
app.config['JWT'] = None

app.register_blueprint(auth_routes)
app.register_blueprint(alarm_routes)
app.register_blueprint(device_routes)
app.register_blueprint(sse_routes)
app.register_blueprint(webpush_routes)



  

