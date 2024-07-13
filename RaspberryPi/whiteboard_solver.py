import requests
from server_address import server_address
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
