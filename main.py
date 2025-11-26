print('packages imported')
import requests as r
import time as t
from datetime import datetime as dt
from datetime import timedelta,date 
import json 
import os
import boto3
import sys
from dotenv import load_dotenv 

from extract import campaigns_extract
from lists_extract import lists_extracts
from load import load
print('loading functions')

print('running extract')
campaigns_extract()
lists_extracts()
print('extract done')

print('running load')
load()
print('load done')

print('script finished')