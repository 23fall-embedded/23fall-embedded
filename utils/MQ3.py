import time
import RPi.GPIO as GPIO


def __init__(pin):
    self.pin_MQ3 = pin
    GPIO.setup(self.pin_MQ3, GPIO.IN)


def check():
    return 1 if GPIO.input(self.pin_MQ3) == 0 else 0
