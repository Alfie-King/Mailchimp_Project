import requests as r
import time as t
from datetime import datetime as dt
import json 
from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

load_dotenv()
API_KEY = os.getenv('API_KEY')
SERVER_PREFIX = os.getenv('SERVER_PREFIX')
extract_timestamp = dt.now().strftime('%Y-%m-%dT%H-%M-%S')

try:
  client = MailchimpMarketing.Client()
  client.set_config({
    "api_key": API_KEY,
    "server": SERVER_PREFIX
  })

  response = client.campaigns.list(
     since_create_time = '2025-10-01T00:00:00+00:00'
  )

  print('Connection Success')
except ApiClientError as error:
  print("Error: {}".format(error.text))

filepath = 'data/mailchimp_campaigns_' + extract_timestamp + '.json'
with open(filepath,'w') as file:
    json.dump(response,file)