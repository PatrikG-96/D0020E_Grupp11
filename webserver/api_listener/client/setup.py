from datetime import datetime
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet import reactor
import treq
import json
import requests

from client.network.AlarmClientFactory import AlarmClientFactory


    
def setup(api_url, username, password, factory=None):
    
    login_url = api_url + "/auth/user/login"
    login_res = requests.post(login_url, {'username' : username, 'password' : password})
    data = login_res.json()
    
    uid = data['userID']
    
    access_url = api_url + "/server/access/request"
    header = {'x-auth-token' : data['accessToken']}
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    form = {"timestamp" : timestamp, "user_id" : data['userID']}
    access_res = requests.post(access_url, form, headers = header)
    server_access = access_res.json()
    
    if 'error' in server_access:
        print(server_access['error'])
    
    host = server_access['ip']
    port = int(server_access['port'])
    token = server_access['token']
    
    print(f"Host: {host}, Port: {port}, Token: {token}")
    
    if factory is None:
        factory = AlarmClientFactory()
    
    factory.id = uid
    factory.username = username
    factory.password = password
    factory.token = token
    factory.jwt = data['accessToken']
    
    reactor.connectTCP(host, port, factory)
    reactor.run()
    