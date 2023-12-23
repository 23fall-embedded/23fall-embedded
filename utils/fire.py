import RPi.GPIO as GPIO
import time

class fire:

    def __init__(self, pin):
        self.pin_fire = pin
        GPIO.setup(self.pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def check(self):
        return 1 if GPIO.input(self.pin_fire) == 0 else 0
