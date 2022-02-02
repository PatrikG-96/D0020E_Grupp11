import sseclient

"""
Purpose:
    Listen to SSE messages from flask API

Requirements:
    API listener and Flask API instances running, api_sim.py ready to run.

Usage:
    Start API listener, start Flask API, start this script, then run the api_sim
    script. This script should print messages if it's working
"""
uid = input("What uid to use? : ")

messages = sseclient.SSEClient("http://localhost:5000/alarm/listen?user_id="+uid)

for msg in messages:
    print(msg)
