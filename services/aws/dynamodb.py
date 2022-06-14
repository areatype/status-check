import boto3
from botocore.exceptions import ClientError
import os
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

db_sites = os.environ['AWS_DB_SITES']
db_stats = os.environ['AWS_DB_STATS']

session = boto3.Session()
ddb = session.resource('dynamodb') 

def ddb_add_website(item,siteID):
    table = ddb.Table(db_sites)
    try: 
        response = table.put_item(
            Item={
                # to generate a random string for siteID, us gen_random(length) in utils.utils
                'siteID': siteID, 
                'info': {
                    'url': item['info']['url'],
                    'wait': item['info']['wait'],
                    'clientID': item['info']['clientID'],
                    'label': item['info']['label']
                }
            })
        pprint(response)

    except ClientError as e:
        pprint(e)

def ddb_add_stats(timestamp, siteID, text, status, clientID,label):
    table = ddb.Table(db_stats)
    try:
        table.put_item(
            Item={
                'timestamp':timestamp,
                'siteID': siteID,
                'info' : {
                    'status': status,
                    'text': text,
                    'clientID': clientID,
                    'label':label
                    }   
            })
    except ClientError as e:
        pprint(e)

def ddb_get(table):
    table = ddb.Table(table)
    response = table.scan()
    data = response['Items']
    return data