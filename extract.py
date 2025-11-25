import requests as r
import time as t
from datetime import datetime as dt
import json 
from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def extract(start_date, before_date): 

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

    date_since = f"{start_date}T00:00:00+00:00"
    date_end = f"{before_date}T23:59:59+00:00"

    response = client.campaigns.list(
      since_create_time = date_since
      , before_create_time = date_end
    )

    print('Connection Success')
  except ApiClientError as error:
    print("Error: {}".format(error.text))

  filepath = 'data/mailchimp_campaigns_' + extract_timestamp + '.json'
  with open(filepath,'w') as file:
      json.dump(response,file)