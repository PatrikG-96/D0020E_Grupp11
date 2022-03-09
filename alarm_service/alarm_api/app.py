from flask import Flask, url_for
from blueprints.auth import auth
from blueprints.alarm import alarm
from blueprints.access import access
from blueprints.monitor import monitor

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(alarm)
app.register_blueprint(access)
app.register_blueprint(monitor)
