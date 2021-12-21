import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

pinLED = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLED,GPIO.OUT)

obj = GPIO.PWM(pinLED,1000)
obj.start(0)

while True:
  for i in range(0,101,5):
    obj.ChangeDutyCycle(i)
    sleep(0.1)
  for i in range(100,-1,-5):
    obj.ChangeDutyCycle(i)
    sleep(0.1)

GPIO.cleanup()