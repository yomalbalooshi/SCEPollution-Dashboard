from django.http import HttpResponse
from django.shortcuts import render
import boto3
import time
import datetime
import random
from django.contrib.sessions.models import Session
import json
#import pymongo
#import sys

DB_NAME = "dummySensorDB"
TBL_NAME = "sensorReadings"
client = boto3.client('timestream-query', region_name='us-east-1' )
def index(request):
    return render(request, "dashboard/index.html")

def qu():
    response = client.query(QueryString = 'Select city,intersectionId, cityType, ROUND(avg(AQI),0) as averageAQI, ROUND(avg(waittime),0) as averageWaittime, sum(cars+busses+trucks) as sumOfVehicles from dummySensorDB."sensorReadings" Group by city,intersectionId,cityType')
    print(response)
def doccall(querykey,queryvalue): #queryCall for documentDB
    cl = pymongo.MongoClient('mongodb://docDBUser:12345678@trafficpollutiondbreg.cluster-cciqodtzbuum.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false')
    db = cl.trafficpollutiondbreg
    col = db.citycollection
    x = col.find_one({querykey: queryvalue})
    return x
def GeoJSONDataCreation(tsquery):
  queryData=tsquery.get('Rows') # list containing raw cities query data
  queryColumns=tsquery.get('ColumnInfo') #list containig raw column info
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

def appendToGeoJSON(tsquery,filename):
    with open(filename,'w') as f:
      f.truncate(0)
      f.write('{"type":"FeatureCollection", \n "features":\n [')
      #f.write('\n{"type": "Feature", \n"properties":')#start of an item in GeoJSON file
      j=0
      while j<len(tsquery):
        f.write('\n{"type": "Feature", \n"properties":'+json.dumps(tsquery[j],indent=4))
        if j<len(tsquery)-1:
          f.write('\n},')
        else:
          f.write('\n}')
        j+=1
      f.write('\n]\n}') #end of GeoJSON file
def st():
    print("Hello")

def test(request):
    res = st()
    return HttpResponse(res)

def res(request):
    result = qu()
    return HttpResponse(result)
