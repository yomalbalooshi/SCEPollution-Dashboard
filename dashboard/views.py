from math import floor
from unittest import result
from django.core.files.storage import default_storage
from urllib.parse import MAX_CACHE_SIZE
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from json import dumps
import boto3
import time
import datetime
import random
from django.contrib.sessions.models import Session
import json
import pymongo
import sys
from pathlib import Path
import os
from botocore.exceptions import ClientError


DB_NAME = "dummySensorDB"
TBL_NAME = "sensorReadings"
client = boto3.client('timestream-query', region_name='us-east-1' )
ts_query=''
tsQueryStartDate='2021-10-22'
tsQueryEndDate='2021-10-22'
cityQuery='Select city,  ROUND(avg(AQI),0) as averageAQI,cityType, ROUND(avg(waittime),0) as averageWaittime, sum(cars+busses+trucks) as sumOfVehicles, sum(busses) as sumOfBusses,sum(trucks) as sumOfTrucks,sum(cars) as sumOfCars from dummySensorDB."sensorReadings" where time BETWEEN TIMESTAMP \''+tsQueryStartDate+' 00:00:00.000000000\' AND TIMESTAMP \''+tsQueryEndDate+' 23:59:59.000000000\' Group by city,cityType ORDER BY averageAQI DESC'
intersectionQuery='Select city, cityType, ROUND(avg(AQI),0) as averageAQI, ROUND(avg(waittime),0) as averageWaittime, sum(cars+busses+trucks) as sumOfVehicles, sum(busses) as sumOfBusses,sum(trucks) as sumOfTrucks,sum(cars) as sumOfCars,intersectionId from dummySensorDB."sensorReadings" where time BETWEEN TIMESTAMP \''+tsQueryStartDate+' 00:00:00.000000000\' AND TIMESTAMP \''+tsQueryEndDate+' 23:59:59.000000000\'  Group by city,intersectionId,cityType'

def index(request):
   url= generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a"], {'Dashboard': {'InitialDashboardId': '4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a'}})
   url2= generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/1c7ee848-d22b-46e9-a4fe-7e4feab20acf"], {'Dashboard': {'InitialDashboardId': '1c7ee848-d22b-46e9-a4fe-7e4feab20acf'}})

   return render(request, "dashboard/index.html", {'AqiDashboard':{'url': url , 'con': 'aqitrafficchart'}, 'CompDashboard':{'url': url2 , 'con': 'comparisonModal2'}})

def mainTimestreamQueryCall(query): #Used to receive timestream Query results
    response = client.query(QueryString = query)
    rqst=GeoJSONDataCreation(response)
    ts_json= json.dumps(rqst)
    return ts_json

def daterange(request):
    if request.method == "POST":
      daterange = request.POST['data']

def doccall(request): #queryCall for documentDB, Temporary
    t=''
    cl = pymongo.MongoClient('mongodb://docDBUser:12345678@trafficpollutiondbreg.cluster-cciqodtzbuum.us-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')
    db = cl.test
    col = db['intersectioncollection']
    x = col.find({"cityID" : "0705bc80-e847-4a93-8220-a346719b12b5"})
    for i in x:
        t+=str(i)
    return HttpResponse(t)
    
def docDBQuery(queryDictionary,collectionname): #queryCall for documentDB, takes dictionary of {"key":"value"} as input
    t=''
    cl = pymongo.MongoClient('mongodb://docDBUser:12345678@trafficpollutiondbreg.cluster-cciqodtzbuum.us-east-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')
    db = cl.test
    col = db[collectionname]
    x = col.find_one(queryDictionary)
    return x
    
def sensorIntersectionPrint(sensorsArrays): #changes sensor array before appending it to GeoJSON
    sensorArray=sensorsArrays
    overallSensorStatus='online' #If one sensor is offline this will switch to offline
    sensorsInformation='"sensors":['
    for i in sensorsArrays:
        sensorsInformation+=str('\n{')
        for k,v in i.items():
            if k=='sensorID':
                sensorsInformation+=str('\n"'+k+'":'+'"'+str(v)+'",')
            if k=='lastPingTime':
                timedifference=datetime.datetime.now()-v
                timedifferenceseconds=timedifference.total_seconds()
                if((timedifferenceseconds/60)/60>1):
                    sensorsInformation+=str('\n"'+k+'":'+'"'+str(v)+'","sensorStatus":"offline"')
                    overallSensorStatus='offline'
                elif((timedifferenceseconds/60)/60<=1):
                    sensorsInformation+=str('\n"'+k+'":'+'"'+str(v)+'","sensorStatus":"online"')
                
        sensorsInformation+=str('},')
    sensorsInformation=sensorsInformation.rstrip(',')
    sensorsInformation+='],"OverallsensorStatus":"'+overallSensorStatus+'"'
    return sensorsInformation

def docDBCityPrint(dbdictionary): #Returns string containing 'city collection' DocumentDB information
    dbDictresult=''
    querylocdbDict={}
    dbDict=docDBQuery(dbdictionary,'citycollection')
    for k,v in dbDict.items():
       if k=='cityID':
           dbDictresult+=str('\n"'+k+'":'+'"'+str(v)+'"')
       if k=='location':
           querylocdbDict.update({"geometry":v})
    return str(dbDictresult+"},"+str('"geometry": {"coordinates": '+str(querylocdbDict['geometry']['coordinates'])+', "type": "'+str(querylocdbDict['geometry']['type'])+'"}'))
    
     
    
def docDBIntersectionPrint(dbdictionary): #Returns string containing 'intersection collection' DocumentDB information
    dbDictresult=''
    querylocdbDict={}
    dbDict=docDBQuery(dbdictionary,'intersectioncollection')
    for k,v in dbDict.items():
       if k=='cityID':
           dbDictresult+=str('\n"'+k+'":'+'"'+str(v)+'",')
       if k=='location':
           querylocdbDict.update({"geometry":v})
       if k=='sensors':
           dbDictresult+=sensorIntersectionPrint(v)
    return str(dbDictresult+"},"+str('"geometry": {"coordinates": '+str(querylocdbDict['geometry']['coordinates'])+', "type": "'+str(querylocdbDict['geometry']['type'])+'"}'))
    
    
    
def featureMagnitude(aqi): #Used to determine color gradient of Heatmap
  if(aqi>0 and aqi<=50):
    return "0.1"
  if(aqi>=51 and aqi<=100):
    return "0.3"
  if(aqi>=101 and aqi<=150):
    return "0.5"
  if(aqi>=151 and aqi<=200):
    return "0.7"
  if(aqi>=201 and aqi<=300):
    return "0.9"
  if(aqi>=301):
    return "1"
  
def intersectionFileGeneration(queryDictList): 
    return intersectionGeoJSONAppend(queryDictList)
    
    
def cityGeoJSONAppend(tscityquery):
    filename = os.path.join(settings.MEDIA_ROOT, "GeoJSON/cities.GeoJSON") 
    f = default_storage.open(os.path.join(settings.MEDIA_ROOT, "GeoJSON/cities.GeoJSON"), 'w+')
    filestring=''
    filestring+=str('{"type":"FeatureCollection", \n "features":\n [') #fixed GeoJSON start line
     #f.write('\n{"type": "Feature", \n"properties":')#start of an item in GeoJSON file
    cqueryinfo=json.loads(tscityquery)
    for i in cqueryinfo:
        filestring+=str('\n{"type": "Feature", \n"properties":{"coordinateType":"city",')#Fixed for each feature
        nameTypeDict={}
        for k, v in i.items():
            filestring+=str('\n"'+k+'":'+'"'+v+'",') #prints each key+value in time stream query
            if k=='city' or k=='cityType':
                nameTypeDict.update({k:v})
        filestring+='"avgHourlyAQI":'+str(AQITimestreamrequest(nameTypeDict))+","
        filestring+=str(docDBCityPrint(nameTypeDict))    
        filestring+=str('},')#closes block of info for a feature
        #f.write(str(docDBQuery({"intersectionId":v}))) 
    filestring=filestring.rstrip(',')
    filestring+=str(']}') #closes entire feature list
    f.write(filestring)
    f.close()
    f = default_storage.open(os.path.join(settings.MEDIA_ROOT, "GeoJSON/cities.GeoJSON"), 'r')
    data = f.read()
    f.close()
    return str(data+tscityquery)
def cityFileGeneration(tscityquery):
    return cityGeoJSONAppend(tscityquery)
    
    
def GeoJSONDataCreation(tsqueryresponse):
  queryData=tsqueryresponse.get('Rows') # list containing raw cities query data
  queryColumns=tsqueryresponse.get('ColumnInfo') #list containig raw column info
  indvRawDataList=[]#list to contain individual raw data
  rawDataList=[]#list to contain all appended raw data
  queryHeaders=[]#list to contain only query headers
  queryDictionaryList=[]#list containing dictionaries of all keys & values
  #temporary dictionary used in function

  #saving only column headers in separate array
  for i in queryColumns: 
      queryHeaders.append(i['Name'])

  #saving arrays of only query data in separate list
  for j in queryData: 
      d=dict(j.items())
      for i in d:
          k=list(d.get(i))
          t=0
          while t<len(k):
              indvRawDataList.append(*k[t].values())
              t+=1
          rawDataList.append(indvRawDataList)
          indvRawDataList=[]

  #appending dictionaries of query keys and values to final query list
  for i in rawDataList:  
    j=0
    tempdic={} 
    while j < len(i):
      tempdic.update({queryHeaders[j]:i[j]})
      j+=1
    queryDictionaryList.append(tempdic.copy())
  return queryDictionaryList
def intersectionGeoJSONAppend(tsquery):
    filename = os.path.join(settings.MEDIA_ROOT, "GeoJSON/intersections.GeoJSON") 
    f = default_storage.open(os.path.join(settings.MEDIA_ROOT, "GeoJSON/intersections.GeoJSON"), 'w+')
    filestring=''
    filestring+=str('{"type":"FeatureCollection", \n "features":\n [') #fixed GeoJSON start line
     #f.write('\n{"type": "Feature", \n"properties":')#start of an item in GeoJSON file
    queryinfo=json.loads(tsquery)
    for i in queryinfo:
        filestring+=str('\n{"type": "Feature", \n"properties":{"coordinateType":"intersection",') #Fixed for each feature
        for k, v in i.items():
            filestring+=str('\n"'+k+'":'+'"'+v+'",') #prints each key+value in time stream query
            if k=='averageAQI':
                filestring+=str('\n"magnitude":'+'"'+featureMagnitude(float(v))+'",')
            if k=='intersectionId':
                filestring+=str(docDBIntersectionPrint({"intersectionID":v}))
        filestring+=str('},')#closes block of info for a feature
        #f.write(str(docDBQuery({"intersectionId":v}))) 
    filestring=filestring.rstrip(',')
    filestring+=str(']}') #closes entire feature list
    #fileStringJSON=json.dumps(json.loads(filestring),indent=4)
    f.write(filestring)
    f.close()
    f = default_storage.open(os.path.join(settings.MEDIA_ROOT, "GeoJSON/intersections.GeoJSON"), 'r')
    data = f.read()
    f.close()
    return str(data)

def st():
    print("Hello")

def aqiColorGenerator(aqi): #color palette for main dashboard table's AQI
  if(aqi>0 and aqi<=50):
    AQIColor='rgb(102, 245, 66)'
  if(aqi>=51 and aqi<=100):
    AQIColor='rgb(255, 247, 28)'
  if(aqi>=101 and aqi<=150):
    AQIColor='rgb(255, 142, 28)'
  if(aqi>=151 and aqi<=200):
    AQIColor='rgb(245, 25, 10)'
  if(aqi>=201 and aqi<=300):
    AQIColor='rgb(143, 10, 245)'
  if(aqi>=301):
    AQIColor='rgb(105, 9, 9)'
  return AQIColor

def tableCreationHTML(ts_query): #Main dashboard table generation
  jsontrial='<table id="MainTableContent"><tr><th class="mainTableHeader">City</th><th class="mainTableHeader">AQI</th><th class="mainTableHeader">City Type</th><th class="mainTableHeader">Wait Time</th><th class="mainTableHeader">Vehicles %</th><th class="mainTableHeader">Common Vehicle Type</th><th class="mainTableHeader">Add to Comparison</th></tr>'
  tsqueryJSON= json.loads(ts_query)
  vehiclesSumArray={}
  sumOfVehicles=0
  vehiclesPercArray={}
  city=''
  cityType=''
  for lis in tsqueryJSON:
       jsontrial+="<tr class='MainTableRow'>"
       for key,val in lis.items():
           if(key=='city'):
             jsontrial+="<td class='MainTableRowData'>"+val+"</td>"
             city=val
           if(key=='cityType'):
             if(val=='res'):
              cityType = val
              jsontrial+="<td class='MainTableRowData'>"+'Residential'+"</td>"
             if(val=='ind'):
              cityType = val
              jsontrial+="<td class='MainTableRowData'>"+'Industrial'+"</td>"
           if(key=='averageAQI'):
            jsontrial+="<td class='MainTableRowData' style='color:"+aqiColorGenerator(float(val))+"';>"+str(int(float(val)))+"</td>"
           if(key=='averageWaittime'):
             jsontrial+="<td class='MainTableRowData'>"+str(round(float(val)/60, 2))+" Minute(s)</td>"
           if(key=='sumOfVehicles'):
             sumOfVehicles=val
           if(key=='sumOfTrucks'):
             vehiclesSumArray['Trucks']=val
           if(key=='sumOfBusses'):
             vehiclesSumArray['Busses']=val
           if(key=='sumOfCars'):
             vehiclesSumArray['Cars']=val
       fin_max = max(vehiclesSumArray, key=vehiclesSumArray.get)
       vehiclesPercArray['percOfCars']=round((float(vehiclesSumArray.get("Cars"))/float(sumOfVehicles))*100, 3)
       vehiclesPercArray['percOfTrucks']=round((float(vehiclesSumArray.get("Trucks"))/float(sumOfVehicles))*100, 3)
       vehiclesPercArray['percOfBusses']=round((float(vehiclesSumArray.get("Busses"))/float(sumOfVehicles))*100, 3)
       jsontrial+="<td class='MainTableRowData'><div class='vehiclePercentageMainBar'><div class='sumOfBusses' style='flex-basis:"+str(vehiclesPercArray['percOfBusses'])+"%' title='Approx. "+str(vehiclesPercArray['percOfBusses'])+"% Busses'></div><div class='sumOfTrucks'  style='flex-basis:"+str(vehiclesPercArray['percOfTrucks'])+"%' title='Approx. "+str(vehiclesPercArray['percOfTrucks'])+"% Trucks'></div><div class='sumOfCars'  style='flex-basis:"+str(vehiclesPercArray['percOfCars'])+"%' title='Approx. "+str(vehiclesPercArray['percOfCars'])+"% Cars'></div></div></td>"
       jsontrial+="<td class='MainTableRowData'>"+str(fin_max)+"</td>"
       jsontrial+="<td><button class='AddToCompareTableButton' value='"+city+ " - " +cityType+"' onClick='Add(value)'>Add to Compare</button></td>"
       jsontrial+="</tr>"
       vehiclesSumArray.clear()  
  jsontrial+="</table>"
  return jsontrial

def res(request):
    ts_query = mainTimestreamQueryCall(cityQuery)
    result= tableCreationHTML(ts_query)
    cityFileGeneration(ts_query)
    tsIntersectoinQuery=mainTimestreamQueryCall(intersectionQuery)
    intersectionFileGeneration(tsIntersectoinQuery)
    return HttpResponse(result)


# Create QuickSight and STS clients
qs = boto3.client('quicksight',region_name='us-east-1')
sts = boto3.client('sts')

def generateEmbedUrlForAnonymousUser(accountId, quicksightNamespace, authorizedResourceArns, experienceConfiguration):
    try:
        response = qs.generate_embed_url_for_anonymous_user(
            AwsAccountId = accountId,
            Namespace = quicksightNamespace,
            AuthorizedResourceArns = authorizedResourceArns,
            ExperienceConfiguration = experienceConfiguration,
            SessionLifetimeInMinutes = 600
        )
            
        return response['EmbedUrl']
        
    except ClientError as e:
        print(e)
        return "Error generating embeddedURL: " + str(e)

    
def AQITimestreamrequest(nameTypeDict):
    printresult=''
    queryresult=''
    city=nameTypeDict['city']
    cityType=nameTypeDict['cityType']
    query="Select ROUND(avg(AQI),0) as averageAQI, EXTRACT(hour from time) as hourOfDay from dummySensorDB.\"sensorReadings\" WHERE city='"+city+"' AND cityType='"+cityType+"' AND time BETWEEN TIMESTAMP '2021-08-09 00:00:00.000000000' AND TIMESTAMP '2021-08-10 00:00:00.000000000' Group by EXTRACT(hour from time) Order by hourOfDay ASC"
    queryresult+=mainTimestreamQueryCall(query)
    printresult=str(queryresult)
    return printresult
