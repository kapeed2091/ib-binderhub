import json
import os
import requests

from utilities.get_hostname import get_hostname
from utilities import LAB_ID

url = 'https://ibeyzvgkq8.execute-api.ap-south-1.amazonaws.com/dev/base'

data = {
  "function_type": "GET",
  "lab_id": LAB_ID,
  "user_id": get_hostname(),
  "object_name": "notebooks.tar"
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    download_url = response.json()['url']

    requests.get(download_url)
    os.system('tar -xvzf notebooks.tar')
except:
    pass
