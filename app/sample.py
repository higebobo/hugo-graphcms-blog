# -*- mode: python -*- -*- coding: utf-8 -*-
import json
import os
import pathlib
import urllib.request

from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = pathlib.Path(APP_DIR).parent

dotenv_path = os.path.join(PROJECT_DIR, '.env')
load_dotenv(dotenv_path)

endpoint = os.getenv('GRAPHCMS_ENDPOINT')
token = os.getenv('GRAPHCMS_TOKEN')
headers = {'Authorization': f'Bearer {token}'}
query = {"query": "{posts {title body}}"}

req = urllib.request.Request(endpoint,
                             data=json.dumps(query).encode(),
                             headers=headers)

with urllib.request.urlopen(req) as response:
    payload = json.loads(response.read())
    status_code = response.getcode()

print (status_code, payload)
