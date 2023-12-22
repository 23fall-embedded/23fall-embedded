import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(15, GPIO.IN)

while True:
    dout = GPIO.input(15)
    if dout == 0:
        print("leaked！")
    else:
        print("not leaked")
    time.sleep(1)
