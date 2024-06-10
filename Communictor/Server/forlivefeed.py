import requests

def live_image_to_server(img_location):
    url = "http://192.168.8.100:80/live"
    files = {'file': open(img_location, 'rb')}
    requests.post(url, files=files)




