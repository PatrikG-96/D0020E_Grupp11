from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.interfaces import IAddress
from typing import Optional
from network.AlarmProtocol import AlarmProtocol
from twisted.python import log
from twisted.internet.defer import Deferred


class AlarmFactory(ServerFactory):
    """An extension of twisted.internet.protocol.ServerFactory. Creates instances of AlarmProtocol for each client connection.
       Successfully authenticated clients will be registered here. Contains methods for sending AlarmNotifications to all clients
       or all clients given a set of client IDs.
       
    Attributes
    ----------
    controller_service : AlarmController
        Used to get callbacks that are defined in the controller module
    clients : dict
        A mapping from client ID to client protocol instance
    d : Deferred
        A Deferred containing callback chain for alerting clients
        
    Methods
    -------
    __makeDeferred() -> Deferred
        Creates a Deferred object with the right callbacks added. Used for resetting self.d
    buildProtocol(addr : IAddress) -> AlarmProtocol
        Creates an instance of AlarmProtocol. Used in internal twisted processes
    sendToAll(message : dict, ids : list = None)
        Triggers self.d with a dictionary containing the message and the id list
    notifyClients(args : dict)
        Callback in callback chain. Receives dictionary from sendToAll. If id list is not None, it sends
        the message to all clients in self.clients with an ID in id list. If id list is None, send to all clients.
    register(proto : AlarmProtocol)
        Add the client connection to self.clients
    deregister(proto : AlarmProtocol)
        Remove the client connetion from self.clients
    """
    protocol = AlarmProtocol
    
    def __init__(self, controller_service):
        """Creates the factory

        Parameters
        ----------
        controller_service : AlarmController
            Controller for parsing and decision that client connection want access to
        """
        self.controller_service = controller_service
        controller_service.registerFactory(self)
        self.d = self.__makeDeferred()
        self.clients = {}
    
    def buildProtocol(self, addr: IAddress) -> "Optional[Protocol]":
        #Default docs should suffice here
        proto = AlarmProtocol(addr, self)
        return proto
    
    def __makeDeferred(self):
        """Creates a Deferred object and adds the appropriate callbacks

        Returns
        -------
            A Deferred object with callbacks added, ready to be triggered
        """
        d = Deferred()
        d.addCallback(self.notifyClients)
        return d
    
    def sendToAll(self, message : dict, ids : list = None):
        """Triggers the process of sending a message to all connected clients or all clients with an ID matching
           the ids parameter

        Parameters
        ----------
        message : dict
            The message to be send. A protocol message in JSON format.
        ids : list
            A list of IDs of the clients to send the message to
        """
        args = {'ids': ids, 'message' : message}
        print(f"ids : {ids}")
        self.d.callback(args)
        self.d = self.__makeDeferred()
    
    def notifyClients(self, args):
        """Callback to be triggered by sendToAll, performs the actual sending

        Parameters
        ----------
        args : dict
            A dictionary created by sendToAll that contains the message and the list of ids
        """
        ids = args['ids']
        message = args['message']
        
        if ids is None:
            for id, client in self.clients.items():
                client.send(message)
        
        for id in ids:
            if id in self.clients:
                log.msg(f"Should send to client: {id}")
                self.clients[id].send(message)
    
    def register(self, proto : AlarmProtocol):
        """Registers the protocol (client connection) in the factory. This means its authenticated and will received notifications

        Parameters
        ----------
        proto : AlarmProtocol
            The protocol to add
        """
        log.msg(f"Client '{proto.client_id}' authorized. Registering.")
        self.clients[int(proto.client_id)] = proto
        
    def deregister(self, proto : AlarmProtocol):
        """Degisters the protocol (client connection) in the factory. This means its no longer authenticated and will 
           not receive any more notifications

        Parameters
        ----------
        proto : AlarmProtocol
            The protocol to remove
        """
        if proto.client_id in self.clients:
            log.msg(f"Client '{proto.client_id}' deregistering.")
            del self.clients[proto.client_id]