import requests
from server_address import server_address

#post image to server
def post_image(image_path):
    url = server_address+'/image'
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image sent successfully")
    else:
        print("Error sending image")
        print(response.text)
    return response.json().get("result")