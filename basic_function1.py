#button * LED * camera


import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pinButton = 22
pinLED = 37

GPIO.setup(pinButton,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(pinLED,GPIO.OUT)

camera = PiCamera()
camera.start_preview()

counter = 1
while True:
  pinStatus = GPIO.input(pinButton)
  if pinStatus == GPIO.LOW:
    camera.capture('/home/pi/Desktop/image%s.jpg' % counter)
    camera.stop_preview()
    sleep(0.5)
    GPIO.output(pinLED,GPIO.HIGH)
    print('push_count:','number of ',counter)
    counter += 1
    sleep(0.5)

  else:
    GPIO.output(pinLED,GPIO.LOW)
    camera.start_preview()

GPIO.cleanup()