import RPi.GPIO as GPIO
import time


class light:
    def __init__(self, pin):
        self.pin_light = pin
        GPIO.setup(self.pin_light, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def check(self):
        return 1 if GPIO.input(self.pin_light) == 0 else 0
