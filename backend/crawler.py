from enum import Enum
import urllib.request
from datetime import datetime
import re

# potential bug for break

# accordion-content-0 accordion-content-1

# basic Shuttle and Shuttle Stop classes
class Shuttle:
    def __init__(self, name, latitude, longitude,websiteUrl):
        self.__name = name
        self.__websiteUrl = websiteUrl
        self.__latitude = latitude
        self.__longitude = longitude
        self.__time_table = []

    def getName(self):
        return self.__name
    
    def getLatitude(self):
        return self.__latitude
    
    def getLongitude(self):
        return self.__longitude
    
    def updateLatitude(self,latitude):
        self.__latitude = latitude

    def updateLongitude(self,longitude):
        self.__longitude = longitude
    
    def fetchDataFromWebsite(self):
        basic_url = 'https://parking.wustl.edu/items/south-campus/'
        Url = basic_url + self.__websiteUrl + '/'
        page = urllib.request.urlopen(Url)
        page_text = str(page.read()) 
        # split all time table
        page_text_all_table = page_text.split('<div class=\"wp-block-washu-accordions accordion\">\\n')[1]
        page_text_all_table = page_text_all_table.split('\\n</div>')[0]
        # split the data into different table
        page_text_different_table = page_text_all_table.split('</dd>')
        all_date = []
        all_location = []
        all_time = []
        for tables in page_text_different_table:
            if len(tables)<50:
                continue
            # get header
            tmpresult = tables.split('</dt>')
            date = tmpresult[0]
            location_content = tmpresult[1]
            date = re.findall(r'\(.+?\)', date)[0]
            date = date.replace("&#8211;","to").replace("(","").replace(")","")
            all_date.append(date)
            # get location
            locationtmp = re.findall(r'<th>.+?<\/th>', location_content)
            location = []
            for lo in locationtmp:
                location.append(lo.replace("&amp;","").replace("<th>","").replace('</th>',"").replace("<br>"," "))
            all_location.append(location)
            # get time
            tmpresult = location_content.split('<tr>')
            all_time_one_Table = []
            for result in tmpresult:
                if "<td>" not in result:
                    continue
                tmptimes = []
                times = result.split('</td>')
                for time in times:
                    if "<td>" not in time:
                        continue
                    time = time.replace("<td>","").replace('</td>',"")
                    tmptimes.append(time)
                all_time_one_Table.append(tmptimes)
            all_time.append(all_time_one_Table)
        result = []
        result.append(all_date)
        result.append(all_location)
        result.append(all_time)
        self.__time_table = result

    def hasShuttleTimeTable(self):
        if(len(self.__time_table)==0):
            self.fetchDataFromWebsite()

        if len(self.__time_table) > 0:
            return True
        else:
            return False
        
    def findShuttleTime(self,day,hour,minute,stop):
        if(len(self.__time_table)==0):
            self.fetchDataFromWebsite()

        tableIndex = 0
        if (int(day)<=0 or int(day) >=6):
            tableIndex = 1

        locationIndex = self.__time_table[1][0].index(stop)
        
        time_string = hour + ':' + minute
        search_time = datetime.strptime(time_string,'%H:%M')

        for time in self.__time_table[2][tableIndex]:
            systemTime = datetime.strptime(time[locationIndex],'%I:%M   %p')
            if systemTime < search_time:
                continue
            else:
                return  ["%s:%s" % (systemTime.hour, systemTime.minute),"%s:%s" % (systemTime.hour-search_time.hour, systemTime.minute-search_time.minute)]
            
        return ["No shuttle today","No shuttle today"]
    
    def getShuttleStop(self):
        return self.__time_table[1][0]
    
        
        

# all shuttles object
Campus_Circulator  = Shuttle('Campus Circulator',0,1,'campus-circulator')
DeBaliviere_Place_Shuttle = Shuttle('DeBaliviere Place Shuttle',0,2,'debaliviere-place')
Delmar_Loop_Shuttle = Shuttle('Delmar Loop Shuttle',1,1,'delmar-loop')
Lewis_Collaborative_Shuttle = Shuttle('Lewis Collaborative Shuttle',2,1,'lewis-center')
Skinker_DeBaliviere_Shuttle = Shuttle('Skinker-DeBaliviere Shuttle',3,1,'skinker-debaliviere')
South_Campus_Shuttle = Shuttle('South Campus Shuttle',4,1,'south-campus')

def updateAllWebsiteData():
    if not(Campus_Circulator.hasShuttleTimeTable() and DeBaliviere_Place_Shuttle.hasShuttleTimeTable() and Delmar_Loop_Shuttle.hasShuttleTimeTable() and Lewis_Collaborative_Shuttle.hasShuttleTimeTable() and Skinker_DeBaliviere_Shuttle.hasShuttleTimeTable() and South_Campus_Shuttle.hasShuttleTimeTable()):
        Campus_Circulator.fetchDataFromWebsite()
        DeBaliviere_Place_Shuttle.fetchDataFromWebsite()
        Delmar_Loop_Shuttle.fetchDataFromWebsite()
        Lewis_Collaborative_Shuttle.fetchDataFromWebsite()
        Skinker_DeBaliviere_Shuttle.fetchDataFromWebsite()
        South_Campus_Shuttle.fetchDataFromWebsite()

    print(Campus_Circulator.getShuttleStop())
    print( DeBaliviere_Place_Shuttle.getShuttleStop())
    print(Delmar_Loop_Shuttle.getShuttleStop())
    print(Lewis_Collaborative_Shuttle.getShuttleStop())
    print(Skinker_DeBaliviere_Shuttle.getShuttleStop())
    print(South_Campus_Shuttle.getShuttleStop())

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