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
otherwise it's rejected.

### The clients
The system is designed to be client neutral in the sense that any type of client following the specified protocols will be able to use the system, as long as they are authorized. We are developing our version of a client, which 
is a web frontend to the system.


## How to install and run the code


## Monitor and adding new sensors



## Authors

- [@Patrik Guthenberg](https://github.com/PatrikG-96)
- [@Alexander Eklund](https://www.github.com/AlexanderEklund)
- [@Astbrq Jamil](https://www.github.com/asta987)
- [@Johan Mölder](https://github.com/EvilCyberMonkey)

