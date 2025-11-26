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

from extract import extract
from load import load
print('loading functions')

print('running extract')
extract()
print('extract done')

print('running load')
load()
print('load done')

print('script finished')