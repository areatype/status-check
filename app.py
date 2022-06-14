import os
import time
import threading
import services.twil.sms as sms
import services.aws.dynamodb as ddb
import requests
from requests.exceptions import HTTPError

from dotenv import load_dotenv
load_dotenv()

db_sites = os.environ['AWS_DB_SITES']

'''
Get a list of websites from the Website DB table
Check status of each in threads w/intervals based on wait value

:param str db:
  The name of the DynamoDB database

'''
def get_website_list(db):
    sites = ddb.ddb_get(db)
    for item in sites:
      url = item['info']['url']
      siteID = item['siteID'] 
      clientID = item['info']['clientID'] 
      label = item['info']['label'] 
      sec = int((item['info']['wait']))
      th = threading.Thread(target=status_check,args=(url,sec,siteID,clientID,label))
      th.start()
    

'''
Check the status of each website
Create an entry for the Stats DB table

:param str url:
  The URL of the the website

:param int sec:
  The delay in seconds between status checks

:param str siteID:
  The unique ID for the website

'''

def status_check(url, sec, siteID, clientID,label):
    while True:
        timestamp = int(round(time.time() * 1000))
        get_result = http_get(url)
        status = get_result['status']
        text = get_result['text']
        if status == 'ok':
            pass
        if status == 'HTTP error':
            msg = url + ' is down! \n HTTP error: ' + text
            sms.sendSMS(msg)
        if status == 'URL error':
            msg = url + ' is not accessible! \n URL error: ' + text 
            sms.sendSMS(msg)
        ddb.ddb_add_stats(timestamp, siteID, text, status, clientID,label)
        time.sleep(sec)
        

'''
Run the URL through a GET request; return the status and message

:param str url:
  The URL to check

'''

def http_get(url):
    status = {}
    try: 
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        status['status'] = 'HTTPError'
        status['text: '] = http_err
    except Exception as err:
        status['status'] = 'nodename nor servname provided'
        status['text'] = err
    else:
        status['status'] = response.status_code
        status['text'] = 'OK'
    return status

get_website_list(db_sites) # this will run infinitely once started