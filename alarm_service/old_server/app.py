from network.AlarmFactory import AlarmFactory
from network.AlarmProtocol import AlarmProtocol
from controller.controller import Controller
from twisted.python import log


def main():

    log.startLogging(open('logs.txt', 'w'))

    controller = Controller()

    factory = AlarmFactory(controller)

    from twisted.internet import reactor
    reactor.listenTCP(3456, factory)
    reactor.run()


if __name__ == "__main__":
    main()
