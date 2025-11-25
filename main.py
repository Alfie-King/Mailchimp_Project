print('packages imported')
import requests as r
import time as t
from datetime import datetime as dt
import json 
import os
import boto3
import sys
from dotenv import load_dotenv 

from extract import extract
from load import load
print('loading functions')

print('running extract')
print('Please input the date window you wish to search for campaigns in')
start_date = input('What is the beginning of the date window you wish to search?')
before_date = input('What is the end of the date window you wish to search?')
extract(start_date, before_date)
print('extract done')

print('running load')
load()
print('load done')

print('script finished')