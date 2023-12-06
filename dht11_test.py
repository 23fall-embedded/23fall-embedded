import RPi.GPIO as GPIO
import utils.dht11 as dht11
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(17)

while True:
    result = instance.read()

    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
    else:
        print("Error: %d" % result.error_code)

    time.sleep(2)
