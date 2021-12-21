import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pinPIR = 7
GPIO.setup(pinPIR, GPIO.IN)

count = 1

while True:
  state = GPIO.input(pinPIR)
  if state == True:
    print('detect infrared:','number of',count)
    count += 1
    sleep(0.3)

GPIO.cleanup()