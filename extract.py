from datetime import datetime as dt
import logging

log_filename = f"logs/extract_{dt.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from datetime import timedelta, date

# Adding extract function so that the code can be run from 1 script
def campaigns_extract(): 

  start_date = date.today()-timedelta(days=90)
  before_date = date.today()

  logger.info("Starting extract function")

  # Loading the .env data to keep private
  load_dotenv()
  API_KEY = os.getenv('API_KEY')
  SERVER_PREFIX = os.getenv('SERVER_PREFIX')
  if not API_KEY or not SERVER_PREFIX:
      logger.error("Missing API_KEY or SERVER_PREFIX in environment variables")
      return

  # Creating extract timestamp so that it can be seen when the data was extracted
  extract_timestamp = dt.now().strftime('%Y-%m-%dT%H-%M-%S')
  logger.info(f"Extract timestamp: {extract_timestamp}")

  # Testing connection to API
  try:
    client = MailchimpMarketing.Client()
    client.set_config({
      "api_key": API_KEY,
      "server": SERVER_PREFIX
    })
    logger.info("Mailchimp client configured")

    date_since = f"{start_date}T00:00:00+00:00"
    date_end = f"{before_date}T23:59:59+00:00"
    logger.info(f"Looking for campaigns between {start_date} to {before_date}")

    response = client.campaigns.list(
      since_create_time = date_since
      , before_create_time = date_end
    )
    logger.info("API request successful")
    print('Connection Success')

    # Downloads the data from the API to the data folder to then be put into S3 by the load function
    import json
    import pandas as pd

    # 1) Save the live API response to a timestamped file
    filepath = f"data/mailchimp_campaigns_{extract_timestamp}.json"
    with open(filepath, "w") as f:
        json.dump(response, f)

    logger.info(f"Data written to {filepath}")

    # 2) Load the same file and normalize the campaigns list into a DataFrame
    with open(filepath) as f:
        data = json.load(f)

    campaigns = data.get("campaigns", [])
    df = pd.json_normalize(campaigns)

    logger.info(f"Extracted {len(df)} campaigns into DataFrame")

  # If connection to the API is bad it outputs this error        
  except ApiClientError as error:
    logger.error(f"Mailchimp API error: {error.text}")
  except Exception as e:
     logger.exception(f"Unexpected error occured: {str(e)}")

