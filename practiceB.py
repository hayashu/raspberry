import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

pinLED = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinLED,GPIO.OUT)

while True:
  x = input("on-off time:")
  y = input("LED keep time:")
  for i in range(1, int(x)+1):
    GPIO.output(pinLED,GPIO.HIGH)
    sleep(float(y))
    GPIO.output(pinLED,GPIO.LOW)
    sleep(float(y))

GPIO.cleanup();
# 緑2  黄色1