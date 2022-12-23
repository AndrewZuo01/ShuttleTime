from enum import Enum
import urllib.request
from datetime import datetime
import re
import json
import geopy.distance


south_list = [
    (38.637011,-90.303662),
    (38.635469, -90.303924),
    (38.633976, -90.309472),
    (38.634352, -90.313398),
    (38.634653, -90.316385)
]

west_list = [
    (38.646698, -90.305956),
    (38.647972, -90.321153),	
    (38.649346, -90.329193),
    (38.650042, -90.331345)
]
skinker_list = [
    (38.650025, -90.300517),
    (38.653575, -90.299888),	
    (38.653337, -90.296351),	
    (38.654122, -90.296142),
    (38.653958, -90.294197),	
    (38.652172, -90.294069),	
    (38.650380, -90.294362)	
]
debaliviere_list = [
    (38.648609, -90.285155), 
    (38.648627, -90.282886), 
    (38.649384, -90.280598), 
    (38.648516, -90.278305), 
    (38.648240, -90.280454)    
]
delmar_list = [
    # need update
    
    (38.650064, -90.300523),
    (38.656555, -90.301642),
    (38.654803, -90.305744),
    (38.655683, -90.310859),
    (38.645497, -90.315272),
    (38.645305, -90.312951)
]
lewis_list = [
    (38.656416, -90.308728),
    (38.658187, -90.308571),
    (38.659186, -90.307359),
    (38.659075, -90.305818),
    (38.658555, -90.303020),
    (38.657345, -90.300730),
    (38.658377, -90.300528)
]
final_list = [[(38.646992, -90.309009)]]

final_list.append(south_list)
final_list.append(west_list)
final_list.append(skinker_list)
final_list.append(debaliviere_list)
final_list.append(delmar_list)
final_list.append(lewis_list)
# v = (38.635469, -90.303925)
shuttle_list_map = ["final","South Campus Shuttle","West Campus Shuttle","Skinker-DeBaliviere Shuttle","DeBaliviere Place Shuttle","Delmar Loop Shuttle","Lewis Collaborative Shuttle"]
# print(closest(final_list[1], v))

def distance(coords_1, coords_2):
    return geopy.distance.geodesic(coords_1, coords_2).m

def closest(data, v):
    return min(data, key=lambda p: distance(v,p))
# potential bug for winter break

# accordion-content-0 accordion-content-1

# basic Shuttle and Shuttle Stop classes

class Shuttle:
    def __init__(self, name, latitude, longitude,websiteUrl,index):
        self.__name = name
        self.__websiteUrl = websiteUrl
        self.__latitude = latitude
        self.__longitude = longitude
        coordinateList = []
        coordinateList.append(final_list[0][0]) 
        for each in final_list[index+1]:
            coordinateList.append(each)
        self.__stopCoordinate = coordinateList
        self.__time_table = []
        self.__reportStop = []
        self.__mapStop = []
        self.__status = ["Normal","default","default"]

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
    # only runs at exact time on sever
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
                    time = time.replace("<td>","").replace('</td>',"").replace('<p>',"").replace('</p>',"")
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
    # read only, no data race
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
            systemTime = datetime.strptime(time[locationIndex].strip(),'%I:%M %p')
            systemTime = datetime.strptime(time[locationIndex].strip(),'%I:%M %p')
            if systemTime < search_time:
                continue
            else:
                minute_value = systemTime.minute
                if  minute_value<10:
                    minute_value = '0' + str(minute_value)
                time = str(systemTime.hour) + ':' + str(minute_value)
                return  [time,systemTime.hour,minute_value]
            
        return ["No more shuttle today","No more shuttle today","No more shuttle today"]
    
    def getShuttleStop(self):
        if(len(self.__time_table) == 0):
            self.fetchDataFromWebsite()
        return self.__time_table[1][0]
    
    def setShuttleStop(self,hour,minute,stop):
        self.__reportStop = [hour,minute,stop]
        # potential bug different day
        
    def findShuttleStop(self,stop):
        if(len(self.__reportStop)==0):
            return ["no reports"]
        result = (datetime.datetime.now().hour() - self.__reportStop[0]) * 60 + (datetime.datetime.now().minute() - - self.__reportStop[1])
        result = "The shuttle is at " + self.__reportStop[2] + " " + str(result) + " minutes ago"
        return result

    def getStopCoordinate(self):
        return self.__stopCoordinate

    def mapUrlLoad(self):
        mapUrl = "https://gis-arcsrv1.wustl.edu/arcgis/rest/services/Hosted/Circulator_Locations_Portal/FeatureServer/0/query?f=json&where=(ignition%20%3D%20%271%27)%20AND%20(visible%20%3D%201)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-10057889.929889776%2C%22ymin%22%3A4657155.259379659%2C%22xmax%22%3A-10018754.171407819%2C%22ymax%22%3A4696291.017861616%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile"
        page = urllib.request.urlopen(mapUrl)
        page = (page.read().decode(page.headers.get_content_charset()))
        dict_obj = json.loads(page)
        return dict_obj
    def getMapData(self):
        self.__mapStop = []
        for drow in self.mapUrlLoad()['features']:
            if(len(drow) < 1):
                return 'no shuttle on map now'
            shuttleName = drow['attributes']['type']
            updateTime = drow['attributes']['lastupdated']
            longitude = drow['attributes']['longitude']
            latitude = drow['attributes']['latitude']
            if(self.__name.find(shuttleName) != -1):
                self.__mapStop.append([shuttleName,updateTime,longitude,latitude])
                
        return self.__mapStop
            # for drowAttribute in drow['attributes']:
            #     # device = re.search(r"\"lastupdated\":\":(.*?) on ", drowAttribute).group(1)
            #     # shuttle = re.search(r"\'type\': \'(.*?)\'", drow[i]).group(1)
            #     print(drowAttribute)
    # result can have data race, try atomicty
    def getMapReport(self):
        self.getMapData()
        if len(self.__mapStop)==0:
            return ["no map report"]
        if not (self.__name in shuttle_list_map):
            return ["no available map report for this shuttle(route too complex)"]
        return self.__mapStop

    def getShuttleStatus(self,status,hour,minute,longitude,latitude):
        if(status != "Normal" and status != "Late" and status != "Early"):
            return self.__status
        else:
            userCoordinate = (latitude,longitude)
            min = 9999999999999
            tmp = self.getStopCoordinate()
            for coor in tmp:
                dis = distance(coor,userCoordinate)
                if(dis < min):
                    min = dis
            if(min > 30):
                return self.__status + "report fail (too far from stops)"
            if(int(minute) < 10):
                minute = "0" + str(minute)
            self.__status = [status,str(hour),str(minute)]
            return self.__status
        
Campus_Circulator  = Shuttle('Campus Circulator',0,1,'campus-circulator',0)
DeBaliviere_Place_Shuttle = Shuttle('DeBaliviere Place Shuttle',0,2,'debaliviere-place',3)
Delmar_Loop_Shuttle = Shuttle('Delmar Loop Shuttle',1,1,'delmar-loop',4)
Lewis_Collaborative_Shuttle = Shuttle('Lewis Collaborative Shuttle',2,1,'lewis-center',5)
Skinker_DeBaliviere_Shuttle = Shuttle('Skinker-DeBaliviere Shuttle',3,1,'skinker-debaliviere',2)
South_Campus_Shuttle = Shuttle('South Campus Shuttle',4,1,'south-campus',0)
West_Campus_Shuttle = Shuttle('West Campus Shuttle',1,1,'west-campus-shuttle',1)

# print(South_Campus_Shuttle.getMapReport())
# print(South_Campus_Shuttle.getMapReport())
# print(South_Campus_Shuttle.getMapReport())
# print(South_Campus_Shuttle.getMapReport())

            # for i in index:
                # if(drow[i] == ''):
                #     continue
                # device = re.search(r"\'devicename\': \'(.*?)\', \'ignition\':", drow[i]).group(1)
                # shuttle = re.search(r"\'type\': \'(.*?)\'", drow[i]).group(1)
                # update = re.search(r"\'lastupdated\': \'(.*?)on 11-27-2022\', \'type\':", drow[i]).group(1)
                # update = datetime.strptime(update.strip(),'%I:%M:%S %p')
                # update = update.hour * 3600 + update.minute * 60 + update.second
                # clean.append([device,shuttle,update])
# def updateAllWebsiteData():
#     if not(Campus_Circulator.hasShuttleTimeTable() and DeBaliviere_Place_Shuttle.hasShuttleTimeTable() and Delmar_Loop_Shuttle.hasShuttleTimeTable() and Lewis_Collaborative_Shuttle.hasShuttleTimeTable() and Skinker_DeBaliviere_Shuttle.hasShuttleTimeTable() and South_Campus_Shuttle.hasShuttleTimeTable()):
#         Campus_Circulator.fetchDataFromWebsite()
#         DeBaliviere_Place_Shuttle.fetchDataFromWebsite()
#         Delmar_Loop_Shuttle.fetchDataFromWebsite()
#         Lewis_Collaborative_Shuttle.fetchDataFromWebsite()
#         Skinker_DeBaliviere_Shuttle.fetchDataFromWebsite()
#         South_Campus_Shuttle.fetchDataFromWebsite()

#     print(Campus_Circulator.getShuttleStop())
#     print( DeBaliviere_Place_Shuttle.getShuttleStop())
#     print(Delmar_Loop_Shuttle.getShuttleStop())
#     print(Lewis_Collaborative_Shuttle.getShuttleStop())
#     print(Skinker_DeBaliviere_Shuttle.getShuttleStop())
#     print(South_Campus_Shuttle.getShuttleStop())




