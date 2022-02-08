import treq
from twisted.internet import reactor

def print_response(arg):

    print(arg)


d = treq.post("http://localhost:5000/alert", {'device_id': 1, 'type': 'fall_confirmed',
                                              'timestamp' : 2, 'coords':(1,2)})
d.addCallback(print_response)

reactor.run()
