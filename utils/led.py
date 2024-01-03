from gpiozero import LED
import time


class led:
    def __init__(self, r, g, y):
        self.ledr = LED(r)
        self.ledg = LED(g)
        self.ledy = LED(y)

    def led_off(self, col):
        if col == "all":
            if self.ledr.is_lit:
                self.ledr.off()
            if self.ledg.is_lit:
                self.ledg.off()
            if self.ledy.is_lit:
                self.ledy.off()
        if col == "red":
            if self.ledr.is_lit:
                self.ledr.off()
        elif col == "green":
            if self.ledg.is_lit:
                self.ledg.off()
        else:
            if self.ledy.is_lit:
                self.ledy.off()

    def led_on(self, col):   
        if col == "all":
            self.ledr.on()
            self.ledg.on()
            self.ledy.on()
        if col == "red":
            self.ledr.on()
        elif col == "green":
            self.ledg.on()
        else:
            self.ledy.on()
