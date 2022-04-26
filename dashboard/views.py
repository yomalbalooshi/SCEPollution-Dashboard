from django.http import HttpResponse
from django.shortcuts import render

import boto3
import time
import datetime
import random
from django.contrib.sessions.models import Session

DB_NAME = "dummyDB"

TBL_NAME = "sensorReadings"

def index(request):
    return render(request, "dashboard/index.html")

client = boto3.client('timestream-query', region_name='us-east-1' )
def qu():
    response = client.query(QueryString = 'SELECT city, intersectionId FROM dummyDB."sensorReadings" WHERE time>=ago(24h) group by city, intersectionId')
    print(response)

def st():
    print("Hello")

def test(request):
    res = st()
    return HttpResponse(res)
# Create your views here.
def res(request):
    result = qu()
    return HttpResponse(result)
