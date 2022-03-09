from network.ApiProtocol import ApiProtocol
from network.ApiFactory import ApiFactory
from controller.ApiControllerService import ApiControllerService
from twisted.python import log
from client.setup import setup
import sys

def main():
    #log.startLogging(open('apilogs.txt', 'w'))
    log.startLogging(sys.stdout)
    controller = ApiControllerService()
    ApiControllerService.supportAlarmType("fall_confirmed")
    factory = ApiFactory(controller, "http://localhost:2000")
    setup("http://localhost:5000", "patrik", "password", factory)
    
if __name__ == "__main__":
    main()