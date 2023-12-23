import RPi.GPIO as GPIO
import time


def __init__(pin):
    self.pin_fire = pin
    GPIO.setup(self.pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def check():
    return 1 if GPIO.input(self.pin_fire) == 0 else 0
