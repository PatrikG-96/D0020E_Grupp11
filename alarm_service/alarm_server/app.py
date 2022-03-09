from twisted.internet import reactor
from network.MonitorFactory import MonitorFactory
from controller.MonitorController import MonitorController
from network.AlarmFactory import AlarmFactory
from controller.AlarmController import AlarmController
from twisted.python import log
from dotenv import load_dotenv, find_dotenv
import os
import sys

def main():
    
    load_dotenv(find_dotenv())
    

    #log.startLogging(open('logs.txt', 'w'))
    log.startLogging(sys.stdout)
    
    alarm_port = int(os.getenv('ALARM_PORT'))
    monitor_port = int(os.getenv('MONITOR_PORT'))
    
    a_controller = AlarmController()
    a_factory = AlarmFactory(a_controller)
    
    m_controller = MonitorController(a_controller)
    m_factory = MonitorFactory(m_controller)
    

    reactor.listenTCP(alarm_port, a_factory)
    reactor.listenTCP(monitor_port, m_factory)
    log.msg(f"Starting alarm server on port: '{alarm_port}' and monitor server on port: '{monitor_port}'.")
    reactor.run()
    
if __name__ =="__main__":
    main()