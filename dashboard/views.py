from django.shortcuts import render
import boto3


DB_NAME = "dummyDB"

TBL_NAME = "sensorReadings"

def index(request):
    return render(request, "dashboard/index.html")
client = boto3.client('timestream-query')
def qu():
    response = client.query(QueryString = 'SELECT * FROM "dummyDB"."sensorReadings" WHERE time between ago(15m) and now() ORDER BY time DESC LIMIT 10 ')
    return render(response, "dashboard/index.html")


# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")


