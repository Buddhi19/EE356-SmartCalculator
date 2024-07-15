import requests
from server_address import server_address
import os
import sys

sys.path.append(os.path.dirname(__file__))

#post image to server
def post_image():
    image_path = "whiteboard/whiteboard.png"
    url = server_address+"/image_whiteboard"
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image sent successfully")
    else:
        print("Error sending image")
        print(response.text)
    
    return response.json().get("result")


def get_ans(exp: str):
    url = server_address + '/calculate'
    data = {'expression': exp}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json().get("result")
        return result
    else:
        return "Error"

def get_plot_image(exp: str):
    url = server_address + '/plot_graph'
    data = {'expression': exp}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('whiteboard/plot.png', 'wb') as f:
            f.write(response.content)
        print("Plot image saved successfully.")
        return 1
    else:
        print("Failed to generate plot image.")
        return 0

def get_transfer_function(exp: str):
    url = server_address + '/transfer_function'
    data = {'expression': exp}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json().get("result")
        numerator = response.json().get("numerator")
        denominator = response.json().get("denominator")
        print(numerator, denominator)
        return numerator, denominator
    else:
        return "Error"