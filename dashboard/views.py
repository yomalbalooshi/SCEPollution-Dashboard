from django.shortcuts import render
import boto3
import aws_cdk.aws_timestream as timestream
import sys, traceback
from botocore.config import Config
from timeit import default_timer as timer
import datetime
import argparse


client = boto3.client('timestream-query')
# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")

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


def run_query(self, query_string):
        try:
            page_iterator = self.paginator.paginate(QueryString=query_string)
            for page in page_iterator:
                self.__parse_query_result(page)
        except Exception as err:
            print("Exception while running query:", err)
            traceback.print_exc(file=sys.stderr)

run_query(client,'SELECT * FROM "dummyDB"."sensorReadings" WHERE time between ago(15m) and now() ORDER BY time DESC LIMIT 10')
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
                print("QueryId: {}".format(queryId))

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