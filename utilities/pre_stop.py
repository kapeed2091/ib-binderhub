import json
import os
import requests

# from utilities.get_hostname import get_hostname
# from utilities import LAB_ID


def write_with_presigned_url(presigned_post_response, file_to_write):
    with open(file_to_write, 'rb') as f:
        files = {'file': (file_to_write, f)}
        requests.post(
            presigned_post_response['url'],
            data=presigned_post_response['fields'],
            files=files
        )
    return


def get_hostname():
    import socket
    hostname = socket.gethostname()
    return hostname.strip('Jupyter-')

LAB_ID = '1'
url = 'https://ibeyzvgkq8.execute-api.ap-south-1.amazonaws.com/dev/base'

data = {
  "function_type": "CREATE",
  "lab_id": LAB_ID,
  "user_id": get_hostname(),
  "object_name": "notebooks.tar"
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    presigned_post_response = response.json()['url']

    os.system('tar -cvzf notebooks.tar notebooks')

    write_with_presigned_url(presigned_post_response, notebooks.tar)
except:
    pass
