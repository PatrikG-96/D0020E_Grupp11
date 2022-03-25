# Monitoring and alarm system in elderly care

## Introduction

This project is for the class D0020E at LTU. It was originally meant to use the Vayyar Home sensor and integrate with an API from DeleHealth. However, this has since been dropped and the system has moved to a generalized alarm system.
The aim of the system is to integrate different kinds of sensors and technologies in the home of an elderly person. It is abstracted into four different parts, the monitor, the server, the rest API and the clients.

### The Monitor

The monitor runs in the home of the elderly and is responsible for communicating directly with the different sensor, for example a WideFind sensor. It is responsible for parsing data from these sensor and making decisions
on whether a situation warrants an alert. For example, a WideFind attached to the waist of an elderly person could detected when the person has fallen. This event would then be reported to the alarm server. Currently, this is
the only functionality implemented. However, the system is designed to be easily extended with new kinds of sensors, especially if they use MQTT to communicate.

### The server

The server receives the alerts from the Monitors. There is no limit to the amount of monitors that can be active at a given time except for performance limitations of our implementation and the Twisted python library.
When receiving an alert, the server will update its database, and if the alert is deemed serious, it will alert all connected clients.

### The REST API

We didn't want to force any client using this system to keep an active TCP connection to our server. Therefore, we built a simple REST API in Flask on top of the same database used by the server. This API makes it easy to
fetch all relevant data, like alarm logs, active alarms and so on. It's also a middle man for clients wanting to connect to the server for live alerts. To make a connection, the client must be authorized by the API, then
it will receive a token that can be used to authorize a connection to the server. In a process described in the Protocol specification PDF, the token is verified by the server, and if successful the connection is accepted,
otherwise it's rejected. The server and API should be run together, as they need to share a database. It is possible to run them on different machines and remotely connect to the database, but it's simpler to run them as
one application.

### The clients

The system is designed to be client neutral in the sense that any type of client following the specified protocols will be able to use the system, as long as they are authorized. We are developing our version of a client, which
is a web frontend to the system.

## How to install and run the code

### Prerequisites

- Python 3.9 installed
- Node.js installed (only for frontend)
- pipenv installed
- MySQL installed

### Database and .env files

To run all parts of this project, you need to have 2 MySQL databases. The Alarm API and server require a shared database as defined in "alarm_service/dev_db.sql". If you intend to run these two on separate machines, they need
still need to connect to the same database. For the frontend, a scaled down version of this database is required, found in "webserver/frontend_db.sql". This database is required for the web API and alarm listener. There are also
a few .env files that need to be manually added. These are not in the git repo as they contained some personal information. Given more time, using .env files would be changed for a more reasonable configuration method.
However, for now he following .env files need to be made.

- "alarm_service/alarm_server/.env"
  - ALARM_PORT="port of alarm side of server"
  - MONITOR_PORT="port of monitor side of server"
  - DB_NAME="name of the database"
  - DB_HOST="address of database, or localhost if local"
  - DB_USER="username for the database"
  - DB_PASSWORD="password for the database"
- "alarm_service/alarm_api/.env"
  - FLASK_APP=app.py
  - FLASK_ENV=development
  - KEY="a 32 byte key in the form of a hex string"
  - SERVER_IP="IP of server if not hosted on the same machine, otherwise just 127.0.0.1"
  - SERVER_PORT="port of the alarm socket of alarm server"
  - DB_NAME="name of the database"
  - DB_HOST="address of database, or localhost if local"
  - DB_USER="username for the database"
  - DB_PASSWORD="password for the database"
- "alarm_service/monitor/.env
  - HOST="IP of alarm server"
  - PORT="port of monitor side of server"
  - TIMEOUT="timeout in seconds for connecting to server"
- "webserver/alarm_listener/.env"
  - DB_NAME="name of the database"
  - DB_HOST="address of database, or localhost if local"
  - DB_USER="username for the database"
  - DB_PASSWORD="password for the database"
- "webserver/api/.env"
  - FLASK_APP=app.py
  - FLASK_ENV=development
  - KEY="a 32 byte key in the form of a hex string"
  - ALARM_API="url to alarm API"
  - DB_NAME="name of the database"
  - DB_HOST="address of database, or localhost if local"
  - DB_USER="username for the database"
  - DB_PASSWORD="password for the database"

### Running the alarm API and server

Alarm server

1. Go to "alarm_service/alarm_server" in a cmd window.
2. Run "pipenv install".
3. Run "pipenv shell".
4. Run "python app.py". Log output should appear in the cmd window, unless logging to a file.

Alarm API

1. Go to "alarm_service/alarm_api" in a cmd window.
2. Run "pipenv install".
3. Run "pipenv shell".
4. Run "flask run". You should see standard flask output

### Running the monitor

Modify the sensor.json file as needed.

1. Go to "alarm_service/monitor" in a cmd window.
2. Run "pipenv install".
3. Run "pipenv shell".
4. Run "python app.py". Log output should appear in the cmd window, unless logging to a file.

### Running the frontend

The web API

1. Go to "webserver/api" in a cmd window.
2. Run "pipenv install".
3. Run "pipenv shell".
4. Run "flask run -p 2000". You should see standard flask output. Port 2000 is used for development purposes.

The alarm listener

1. Make sure the web API, alarm API and alarm server is started.
2. Go to "webserver/alarm_listener" in a cmd window.
3. Run "pipenv install".
4. Run "pipenv shell".
5. Run "python app.py". Log output should appear in the cmd window, unless logging to a file.
6. Wait for a moment and verify that the connection is successful. When the process is complete, you should see a POST request to the "/auth/client/connected" route in the web API window.

The website

1. Go to "webserver/src" in a new cmd window
2. Run "npm install"
3. Run "npm run start"
4. Wait for the development server to start.

### Testing the system without access to WideFind sensors

1. Perform the setup as described above, skipping the monitor step.
2. Run "test_scripts/sensor_alert_test.py".
3. The alarm should be displayed on the 3D view in the browser.
   Coordinates can be changed manually in the script to test different positions.

## Monitor and adding new sensors

To support additional sensors, you must extend the Sensor class in the Monitor module. See documentation for more details

## Dependencies

All dependencies are resolved by virutal enviroments, but for the sake of completionism all third party dependencies are listed here

### Monitor

- [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### The server and API

- [Flask](https://github.com/pallets/flask)
- [Twisted](https://github.com/twisted/twisted)
- [SQLAlchemy](https://github.com/sqlalchemy)
- [MySQLClient](https://github.com/PyMySQL/mysqlclient)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [bcrypt](https://github.com/pyca/bcrypt)
- [py-jwt](https://github.com/jpadilla/pyjwt)
- [Marshmallow](https://github.com/marshmallow-code/marshmallow)

### The web frontend

- [react](https://github.com/facebook/react)
- [MUI](https://github.com/mui/material-ui)
- [three](https://github.com/mrdoob/three.js)
- [react-three-fiber](https://github.com/pmndrs/react-three-fiber)
- [drei](https://github.com/pmndrs/drei)
- [axios](https://github.com/axios/axios)

## Authors

- [@Patrik Guthenberg](https://github.com/PatrikG-96)
- [@Alexander Eklund](https://www.github.com/AlexanderEklund)
- [@Astbrq Jamil](https://www.github.com/asta987)
- [@Johan Mölder](https://github.com/EvilCyberMonkey)
