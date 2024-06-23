#send an image to server
import requests
from app import host_url

def send_image_to_server(img_location):
    url = "http://192.168.1.4:80/image"
    files = {'file': open(img_location, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        result =  response.json().get("result")
        print(result)
    else:
        print("Error in sending image")

def main():
    image_path = "test12.png"
    send_image_to_server(image_path)

if __name__ == "__main__":
    main()
    