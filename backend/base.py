import time
from flask import Flask
from flask_cors import CORS
from flask import request
import crawler
# python3 -m venv env
# source env/bin/activate
# flask run
api = Flask(__name__)
CORS(api)

Campus_Circulator  = crawler.Shuttle('Campus Circulator',0,1,'campus-circulator')
DeBaliviere_Place_Shuttle = crawler.Shuttle('DeBaliviere Place Shuttle',0,2,'debaliviere-place')
Delmar_Loop_Shuttle = crawler.Shuttle('Delmar Loop Shuttle',1,1,'delmar-loop')
Lewis_Collaborative_Shuttle = crawler.Shuttle('Lewis Collaborative Shuttle',2,1,'lewis-center')
Skinker_DeBaliviere_Shuttle = crawler.Shuttle('Skinker-DeBaliviere Shuttle',3,1,'skinker-debaliviere')
South_Campus_Shuttle = crawler.Shuttle('South Campus Shuttle',4,1,'south-campus')

@api.route('/shuttle', methods=['GET', 'POST'])
def getResult():
    value = request.get_json()
    shuttle = value['shuttle']
    day = value['day'] 
    hour = value['hour'] 
    minute = value['minute'] 
    stop = value['stop'] 
    result = findShuttle(shuttle,day,hour,minute,stop)
    response_body = {
        "time" : result[0],
        "hour" : result[1],
        "minute": result[2],
    }
    return response_body

@api.route('/test')
def findStop():
    return "not yet implemented"

def findShuttle(shuttle,day,hour,minute,stop):
    if(shuttle == "Campus Circulator"):
        return  Campus_Circulator.findShuttleTime(day,hour,minute,stop)
    if(shuttle == "DeBaliviere Place Shuttle"):
        return  DeBaliviere_Place_Shuttle.findShuttleTime(day,hour,minute,stop)
    if(shuttle == "Delmar Loop Shuttle"):
        return  Delmar_Loop_Shuttle.findShuttleTime(day,hour,minute,stop)
    if(shuttle == "Lewis Collaborative Shuttle"):
        return  Lewis_Collaborative_Shuttle.findShuttleTime(day,hour,minute,stop)
    if(shuttle == "Skinker-DeBaliviere Shuttle"):
        return  Skinker_DeBaliviere_Shuttle.findShuttleTime(day,hour,minute,stop)
    if(shuttle == "South Campus Shuttle"):
        return  South_Campus_Shuttle.findShuttleTime(day,hour,minute,stop)


    