import json
import os
import requests

# from utilities.get_hostname import get_hostname
# from utilities import LAB_ID


def get_hostname():
    import socket
    hostname = socket.gethostname()
    return hostname.strip('jupyter-')


LAB_ID = '1'
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

    response = requests.get(download_url)
    with open('/home/jovyan/notebooks.tar', 'wb') as f:
        f.write(response.content)

    os.system('tar -xvzf /home/jovyan/notebooks.tar')
except Exception as e:
    print('Exception in post_start:', e)
    pass
