from flask import Flask, url_for
from blueprints.auth import auth
from blueprints.alarm import alarm

app = Flask(__name__)

app.register_blueprint(auth)
app.register_blueprint(alarm)
