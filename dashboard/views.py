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
    url= generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a"], {'Dashboard': {'InitialDashboardId': '4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a'}})
    url2= generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/1c7ee848-d22b-46e9-a4fe-7e4feab20acf"], {'Dashboard': {'InitialDashboardId': '1c7ee848-d22b-46e9-a4fe-7e4feab20acf'}})

    print(url)

    return render(request, "dashboard/index.html", {'AqiDashboard':{'url': url , 'con': 'embeddingContainerAQI'}, 'CompDashboard':{'url': url2 , 'con': 'embeddingContainerComp'}})

def url(request):
    url= generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a"], {'Dashboard': {'InitialDashboardId': '4c3cc90a-da1a-4fd8-8d7c-88f320b34e5a'}})

    print(url)

    return render(request, "dashboard/index.html", {'url':[url]})



def qu():
    #response = client.query(QueryString = 'SELECT city, intersectionId FROM dummyDB."sensorReadings" group by city, intersectionId')
    
 
    #result_str = executeQuery(client, SELECT city, intersectionId FROM dummyDB."sensorReadings" group by city, intersectionId, timing=True)
    #print(str(result_str))
    #res2 = str(result_str)
    #resp_dict = json.loads(res2)
   # print(result_str)
    #print("Next")
    #url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/59e9a534-0605-47f4-8fe4-110f2646150a"], {'Dashboard': {'InitialDashboardId': '59e9a534-0605-47f4-8fe4-110f2646150a'}})
    url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/597408e3-5d0a-4098-82ec-95efd73035ed"], {'Dashboard': {'InitialDashboardId': '597408e3-5d0a-4098-82ec-95efd73035ed'}})

    print(url)
    HTTPResponse(url)
"""
def run_query(self, query):
        try:
            pageIterator = paginator.paginate(QueryString=query)
            for page in pageIterator:
                self.__parse_query_result(page)
        except Exception as err:
            print("Exception while running query:", err)
            traceback.print_exc(file=sys.stderr) 
"""
def st():
    print("Hello")

def test(request):
    url = generateEmbedUrlForAnonymousUser("234810267545", "default", ["arn:aws:quicksight:us-east-1:234810267545:dashboard/597408e3-5d0a-4098-82ec-95efd73035ed"], {'Dashboard': {'InitialDashboardId': '597408e3-5d0a-4098-82ec-95efd73035ed'}})
    #res = run_query(client,'SELECT city, intersectionId FROM dummyDB."sensorReadings" WHERE time>=ago(24h) group by city, intersectionId')
    return HttpResponse(url)

# Create your views here.
def res(request):
    result = qu()
    #result = run_query(client,'SELECT city, intersectionId FROM dummyDB."sensorReadings" WHERE time>=ago(24h) group by city, intersectionId')

    return HttpResponse(result)
"""
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
"""


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

