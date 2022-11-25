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
    result = crawler.findShuttle(shuttle,day,hour,minute,stop)
    response_body = {
        "time" : result[0],
        "hour" : result[1],
        "minute": result[2],
    }
    return response_body

@api.route('/test')
def findStop():
    return "not yet implemented"