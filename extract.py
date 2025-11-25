import requests as r
import time as t
from datetime import datetime as dt
import json 
from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Adding extract function so that the code can be run from 1 script
def extract(start_date, before_date): 

  # Loading the .env data to keep private
  load_dotenv()
  API_KEY = os.getenv('API_KEY')
  SERVER_PREFIX = os.getenv('SERVER_PREFIX')

  # Creating extract timestamp so that it can be seen when the data was extracted
  extract_timestamp = dt.now().strftime('%Y-%m-%dT%H-%M-%S')

  # Testing connection to API
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

    # Downloads the data from the API to the data folder to then be put into S3 by the load function
    filepath = 'data/mailchimp_campaigns_' + extract_timestamp + '.json'
    with open(filepath,'w') as file:
        json.dump(response,file)

  # If connection to the API is bad it outputs this error        
  except ApiClientError as error:
    print("Error: {}".format(error.text))

