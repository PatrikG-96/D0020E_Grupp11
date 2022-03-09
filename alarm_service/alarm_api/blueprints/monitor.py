
from flask import Blueprint

from database.database import getAllMonitors
from blueprints.decorators.auth_decorator import token_required


monitor = Blueprint('monitor', __name__)

def __format_monitor(db_result):
    
    res = {}
    
    for entry in db_result:
        res[entry.monitorID] = entry.name
        
    return res
    

@monitor.route("/monitor/all")
@token_required
def get_all_monitors():
    
    res = getAllMonitors()    
    
    return __format_monitor(res)
