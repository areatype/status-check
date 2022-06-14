import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone = os.environ['TWILIO_PHONE']
client = Client(account_sid, auth_token)

''' 
This test app only has one account, so cell # is stored as an env variable
For an app with multiple accounts, store cell # in DB along with other account data
'''
sms_user = os.environ['USER1_CELL']


''' 
Send SMS via Twilio service

:param str body:
  The text content of the message

:param str recipient:
  recipient SMS number

:param list media:
  list of URLs to hosted media

'''

def sendSMS(body,media=[],recipient=sms_user):
    message = client.messages \
        .create(
            body=body,
            from_=twilio_phone,
            to=recipient,
            media_url=media
        )
    return message.sid