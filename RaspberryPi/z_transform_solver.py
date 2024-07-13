import os
import sys
import requests

sys.path.append(os.path.dirname(__file__))
from server_address import server_address

def get_z_transform(expression:str):
    url = server_address+'/z_transform_image'
    data = {'expression': expression}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('integrals/z_transform.png', 'wb') as f:
            f.write(response.content)
        print("Z transform image saved successfully.")
    else:
        print("Failed to generate Z transform image.")