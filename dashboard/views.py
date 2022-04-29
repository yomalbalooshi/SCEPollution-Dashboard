from typing import Any
from django.http import HttpResponse
from django.shortcuts import render
import json
from botocore.config import Config
import sys, traceback
from timeit import default_timer as timer
import numpy as np
import os
from collections import defaultdict, namedtuple
import argparse
import boto3
import time
import datetime
import random
from django.contrib.sessions.models import Session
from urllib3 import HTTPResponse

DB_NAME = "dummyDB"

TBL_NAME = "sensorReadings"


def index(request):
    url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/59e9a534-0605-47f4-8fe4-110f2646150a"], {'Dashboard': {'InitialDashboardId': '59e9a534-0605-47f4-8fe4-110f2646150a'}})

    return render(request, "dashboard/index.html", {'url':[url]})

client = boto3.client('timestream-query', region_name='us-east-1' )
paginator = client.get_paginator('query')
response = client.query(QueryString = 'SELECT city, intersectionId FROM dummyDB."sensorReadings" group by city, intersectionId')


def __init__(self, client):
        self.client = client
        self.paginator = client.get_paginator('query')
#pageIterator = paginator.paginate(QueryString=query)

def url(request):
    url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/597408e3-5d0a-4098-82ec-95efd73035ed"], {'Dashboard': {'InitialDashboardId': '597408e3-5d0a-4098-82ec-95efd73035ed'}})
    return render(request, "dashboard/index.html", {'url':[url]})


def qu():
    response = client.query(QueryString = 'SELECT city, intersectionId FROM dummyDB."sensorReadings" group by city, intersectionId')
    
 
    #result_str = executeQuery(client, """SELECT city, intersectionId FROM dummyDB."sensorReadings" group by city, intersectionId""", timing=True)
    #print(str(result_str))
    #res2 = str(result_str)
    #resp_dict = json.loads(res2)
   # print(result_str)
    #print("Next")
    print(response['Rows'])
    HTTPResponse(response['Rows'])
    url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/59e9a534-0605-47f4-8fe4-110f2646150a"], {'Dashboard': {'InitialDashboardId': '59e9a534-0605-47f4-8fe4-110f2646150a'}})
    url2 = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/597408e3-5d0a-4098-82ec-95efd73035ed"], {'Dashboard': {'InitialDashboardId': '597408e3-5d0a-4098-82ec-95efd73035ed'}})

    print(url,url2)
    HTTPResponse(url)

"""def run_query(self, query):
        try:
            pageIterator = paginator.paginate(QueryString=query)
            for page in pageIterator:
                self.__parse_query_result(page)
        except Exception as err:
            print("Exception while running query:", err)
            traceback.print_exc(file=sys.stderr) """

def st():
    print("Hello")

def test(request):
    #res = st()
    #res = run_query(client,'SELECT city, intersectionId FROM dummyDB."sensorReadings" WHERE time>=ago(24h) group by city, intersectionId')
    return HttpResponse(res)
# Create your views here.
def res(request):
    result = qu()
    #result = run_query(client,'SELECT city, intersectionId FROM dummyDB."sensorReadings" WHERE time>=ago(24h) group by city, intersectionId')

    return HttpResponse(result)

## Timestream

def createQueryClient(region, profile = None):
    if profile == None:
        print("Using credentials from the environment")

    print(region)
    config = Config()
    if profile != None:
        session = boto3.Session(profile_name = profile)
        client = session.client(service_name = 'timestream-query',
                                region_name = region, config = config)
    else:
        session = boto3.Session()
        client = session.client(service_name = 'timestream-query',
                                region_name = region, config = config)

    return client

def parseDatum(c_type, data):
    if ('ScalarType' in c_type):
        return parseScalar(c_type['ScalarType'], data.get('ScalarValue'))
    elif ('ArrayColumnInfo' in c_type):
        return parseArrayData(c_type['ArrayColumnInfo'], data.get('ArrayValue'))
    elif ('TimeSeriesMeasureValueColumnInfo' in c_type):
        return parseTSData(c_type['TimeSeriesMeasureValueColumnInfo'], data.get('TimeSeriesValue'))
    elif ('RowColumnInfo' in c_type):
        return parseRowData(c_type['RowColumnInfo'], data.get('RowValue'))
    else:
        raise Exception("All the data is Null???")

def parseScalar(c_type, data):
    if data == None:
        return None
    if (c_type == "VARCHAR"):
        return data
    elif (c_type == "BIGINT"):
        return int(data)
    elif (c_type == "DOUBLE"):
        return float(data)
    elif (c_type == "INTEGER"):
        return int(data)
    elif (c_type == "BOOLEAN"):
        return bool(data)
    elif (c_type == "TIMESTAMP"):
        return data
    else:
        return data

def parseArrayData(c_type, data):
    if data == None:
        return None
    datum_list = []
    for elem in data:
        datum_list.append(parseDatum(c_type['Type'], elem))
    return datum_list

def parseTSData(c_type, data):
    if data == None:
        return None
    datum_list = []
    for elem in data:
        ts_data = {}
        ts_data['time'] = elem['Time']
        ts_data['value'] = parseDatum(c_type['Type'], elem['Value'])
        datum_list.append(ts_data)
    return datum_list

def parseRowData(c_types, data):
    if data == None:
        return None
    datum_dict = {}
    for c_type, elem in zip(c_types, data['Data']):
        datum_dict[c_type['Name']] = parseDatum(c_type['Type'], elem)
    return datum_dict

def flatModelToDataframe(items):
    """
    Translate a Timestream query SDK result into a Pandas dataframe.
    """
    return_val = defaultdict(list)
    for obj in items:
        for row in obj.get('Rows'):
            for c_info, data in zip(obj['ColumnInfo'], row['Data']):
                c_name = c_info['Name']
                c_type = c_info['Type']
                return_val[c_name].append(parseDatum(c_type, data))

    df = return_val
    return df

## Execute the passed query using the client and return the result
## as a dataframe.
def executeQueryAndReturnAsDataframe(client, query, timing = False, logFile = None):
    return flatModelToDataframe(executeQuery(client, query, timing, logFile))

## Executed the passed query using the specified client.
## logFile is a file handle which if initialized is assumed to be a valid file handle
## where messages will be written. The file handle is expected to have been opened
## by the caller. This function does not close the handle and passes it back to the caller.
def executeQuery(client, query, timing = False, logFile = None):
    try:
        pages = None
        queryId = None
        firstResult = None
        start = timer()
        ## Create the paginator to paginate through the results.
        paginator = client.get_paginator('query')
        pageIterator = paginator.paginate(QueryString=query)
        emptyPages = 0
        pages = list()
        lastPage = None
        for page in pageIterator:
            if 'QueryId' in page and queryId == None:
                queryId = page['QueryId']
                print("QueryId: {}".format(queryId) + "Test")

            lastPage = page

            if 'Rows' not in page or len(page['Rows']) == 0:
                ## We got an empty page.
                emptyPages +=1
            else:
                pages.append(page)
                if firstResult == None:
                    ## Note the time when the first row of result was received.
                    firstResult = timer()

        ## If there were no result, then return the last empty page to carry over the query results context
        if len(pages) == 0 and lastPage != None:
            pages.append(lastPage)
        return pages
    except Exception as e:
        if queryId != None:
            ## Try canceling the query if it is still running
            print("Attempting to cancel query: {}".format(queryId))
            try:
                client.cancel_query(query_id=queryId)
            except:
                pass
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        if e.response != None:
            queryId = None
            print("RequestId: {}".format(e.response['ResponseMetadata']['RequestId']))
            if 'QueryId' in e.response:
                queryId = e.response['QueryId']
            print("QueryId: {}".format(queryId))
        raise e
    except KeyboardInterrupt:
        if queryId != None:
            ## Try canceling the query if it is still running
            print("Attempting to cancel query: {}".format(queryId))
            try:
                client.cancel_query(query_id=queryId)
            except:
                pass
        raise
    finally:
        end = timer()
        if timing == True:
            now = datetime.datetime.utcnow()
            if firstResult != None:
                timeToFirstResult = firstResult - start
                timeToReadResults = end - firstResult
            else:
                timeToFirstResult = end - start
                timeToReadResults = 0

            timingMsg = "{}. QueryId: {} Time: {}. First result: {}. Time to read results: {}.".format(now.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                                       queryId, round(end - start, 3), round(timeToFirstResult, 3), round(timeToReadResults, 3))
            print(timingMsg)
            if logFile != None:
                logFile.write("{}\n".format(timingMsg))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'TimestreamQuery', description='Execute a query on Amazon Timestream.')

    parser.add_argument('--endpoint', '-e', action = "store", required = True, help="Specify the service endpoint. E.g. 'us-east-1'")
    parser.add_argument('--profile', action = "store", type = str, default= None, help = "The AWS Config profile to use.")

    args = parser.parse_args()
    print(args)

    client = createQueryClient(args.endpoint, profile=args.profile)
    result = executeQuery(client, """SELECT now()""", timing=True)
    print(str(result))

import json
import boto3
from botocore.exceptions import ClientError
import time

# Create QuickSight and STS clients
qs = boto3.client('quicksight',region_name='us-east-1')
sts = boto3.client('sts')

# Function to generate embedded URL for anonymous user
# accountId: YOUR AWS ACCOUNT ID
# quicksightNamespace: VALID NAMESPACE WHERE YOU WANT TO DO NOAUTH EMBEDDING
# authorizedResourceArns: DASHBOARD ARN LIST TO EMBED
# experienceConfiguration: DASHBOARD ID TO WHICH THE CONSTRUCTED URL POINTS
# sessionTags: SESSION TAGS USED FOR ROW-LEVEL SECURITY
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

