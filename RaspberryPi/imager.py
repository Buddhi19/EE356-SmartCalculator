#takes images from raspberry pi camera and sends them to the server
from picamera2 import Picamera2, Preview
from time import sleep
from libcamera import controls

picam2 = Picamera2()
picam2.start()

picam2.capture_file("image.jpg")