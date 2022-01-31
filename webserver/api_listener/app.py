from network.ApiProtocol import ApiProtocol
from network.ApiFactory import ApiFactory
from controller.ApiControllerService import ApiControllerService
from twisted.python import log

def main():
    log.startLogging(open('apilogs.txt', 'w'))
    controller = ApiControllerService()
    factory = ApiFactory(controller, "http://localhost:5000/alert?user_id=1")
    from twisted.internet import reactor
    reactor.listenTCP(9999, factory)
    print("starting server")
    reactor.run()
    
    
if __name__ == "__main__":
    main()