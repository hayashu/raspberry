import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pinButton = 22
pinLED = 37

GPIO.setup(pinButton,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(pinLED,GPIO.OUT)

pinStatus = 0
GPIO.add_event_detect(pinButton,GPIO.RISING,bouncetime=200)

while True:
  if GPIO.event_detected(pinButton):
    pinStatus = (pinStatus+1)%2
    if pinStatus == 1:
      print('turn on LED')

    else:
      print('turn off LED')
    GPIO.output(pinLED,pinStatus)
GPIO.remove_event_detect(pinButton)

GPIO.cleanup()