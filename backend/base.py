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



@api.route('/shuttle', methods=['GET', 'POST'])
def getResult():
    value = request.get_json()
    shuttle = value['shuttle']
    day = value['day'] 
    hour = value['hour'] 
    minute = value['minute'] 
    stop = value['stop'] 
    result = findShuttleTime(shuttle,day,hour,minute,stop)
    response_body = {
        "time" : result[0],
        "hour" : result[1],
        "minute": result[2],
    }
    return response_body

# @api.route('/setstop')
# def setStop():
#     value = request.get_json()
#     shuttle = value['shuttle']
#     hour = value['hour'] 
#     minute = value['minute'] 
#     stop = value['stop'] 
#     setShuttleStop(shuttle,hour,minute,stop)

@api.route('/report', methods=['GET', 'POST'])
def setStop():
    value = request.get_json()
    shuttle = value['shuttle']
    status = value['status']
    hour = value['hour'] 
    minute = value['minute'] 
    result = findShuttleStatus(shuttle,status,hour,minute)
    response_body = {
        "report": result
    }
    return response_body

# @api.route('/findstop')
# def findStop():
#     value = request.get_json()
#     shuttle = value['shuttle']
#     stop = value['stop'] 
#     result = findShuttleStop(shuttle,stop)
#     response_body = {
#         "result" : result
#     }
#     return response_body

@api.route('/findmap', methods=['GET', 'POST'])
def findMap():
    value = request.get_json()
    shuttle = value['shuttle']
    # avoid race condition
    check = value['check'] 
    result = findShuttleMap(shuttle,check)
    response_body = {
        "result" : result
    }
    return response_body

def findShuttle(shuttle):
    if(shuttle == "Campus Circulator"):
        return  crawler.Campus_Circulator
    if(shuttle == "DeBaliviere Place Shuttle"):
        return  crawler.DeBaliviere_Place_Shuttle
    if(shuttle == "Delmar Loop Shuttle"):
        return  crawler.Delmar_Loop_Shuttle
    if(shuttle == "Lewis Collaborative Shuttle"):
        return  crawler.Lewis_Collaborative_Shuttle
    if(shuttle == "Skinker-DeBaliviere Shuttle"):
        return  crawler.Skinker_DeBaliviere_Shuttle
    if(shuttle == "South Campus Shuttle"):
        return  crawler.South_Campus_Shuttle
    if(shuttle == "West Campus Shuttle"):
        return  crawler.West_Campus_Shuttle

def findShuttleTime(shuttle,day,hour,minute,stop):
    return findShuttle(shuttle).findShuttleTime(day,hour,minute,stop)
    

def findShuttleStop(shuttle,hour,minute,stop):
    return findShuttle(shuttle).findShuttleStop(stop)
    
def setShuttleStop(shuttle,hour,minute,stop):
    return findShuttle(shuttle).setShuttleStop(hour,minute,stop)

def findShuttleMap(shuttle,check):
    if(check == "c"):
        return findShuttle(shuttle).getMapReport()
    return ["no map report"]
def findShuttleStatus(shuttle,status,hour,minute):
    return findShuttle(shuttle).getShuttleStatus(status,hour,minute)



    