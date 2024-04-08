from PIL import Image
import requests
from io import BytesIO
import os
import sys
import datetime

output = "camera.png"

# not checked
def get_image_and_save(ip_address:str):
    """
    download image from webserver and 
    save it as camera.png
    """
    url = ip_address+"/cam-hi.jpg" 

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    try:
        img.save(output,"PNG")
    except:
        print("Error saving image")
    