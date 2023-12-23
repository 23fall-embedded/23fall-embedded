import time
import RPi.GPIO as GPIO


class MQ3:
    def __init__(self, pin):
        self.pin_MQ3 = pin
        GPIO.setup(self.pin_MQ3, GPIO.IN)

    def check(self):
        return 1 if GPIO.input(self.pin_MQ3) == 0 else 0
