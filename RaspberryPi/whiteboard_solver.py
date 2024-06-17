import requests

#post image to server
def post_image():
    image_path = "whiteboard\\whiteboard.png"
    url = "http://192.168.8.101:80/image_whiteboard"
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Image sent successfully")
    else:
        print("Error sending image")
        print(response.text)
    
    return response.json().get("result")
