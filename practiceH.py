from picamera import PiCamera
from time import sleep

cam = PiCamera()
cam.framerate = 15
cam.start_preview()
cam.resolution = (2592,1944)

counter = 1
for i in range(0,100,20):
  cam.annotate_text = "Brightness = %s" % 1
  cam.brightness = i
  sleep(1)
  cam.capture('/home/pi/Downloads/IMG%s.jpg' % counter)
  counter += 1

cam.resolution = (1920,1080)
cam.start_recording('/home/pi/Downloads/video.h264')
sleep(5)
cam.start_recording()
cam.stop_preview()