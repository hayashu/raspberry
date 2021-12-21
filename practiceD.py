import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pinButton = 22
pinLED = 37

GPIO.setup(pinButton,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(pinLED,GPIO.OUT)

counter = 1
while True:
  pinStatus = GPIO.input(pinButton)
  if pinStatus == GPIO.LOW:
    GPIO.output(pinLED,GPIO.HIGH)
    print('push_count:','number of ',counter)
    counter += 1
    sleep(0.5)

  else:
    GPIO.output(pinLED,GPIO.LOW)

GPIO.cleanup()