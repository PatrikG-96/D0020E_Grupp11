from database import *
from database import setNewSubscription
from database import getAllMonitors

res = getAllMonitors()


for a in res:
    print(a.monitorID)