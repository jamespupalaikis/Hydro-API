from picamzero import Camera
import time

cam = Camera()
print("camera set up")

time.sleep(2)
cam.take_photo("pictures/test1.jpg")
print("photo")
