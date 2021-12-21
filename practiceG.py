import Adafruit_DHT
from time import sleep

DHT_SENSPR = Adafruit_DHT.DHT11
DHT_PIN = 16

i = 0

while i < 5:
  humidity, temperature = Adafruit_DHT.read(DHT_SENSPR,DHT_PIN)

  if humidity is not None and temperature is not None:
    print('tempureture={0:0.1f}C moist={1:0.1f}%'.format(temperature,humidity))
  
  else:
    print('senser error occurred. confirm ur cercle.')
    
  i += 1
  sleep(3)