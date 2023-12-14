from gpiozero import LED
import time

ledr = LED(16)
ledg = LED(21)
ledy = LED(20)


def led_off():
    if ledr.is_lit:
        ledr.off()
    if ledg.is_lit:
        ledg.off()
    if ledy.is_lit:
        ledy.off()


def led_on(col):
    led_off()
    if col == "all":
        ledr.on()
        ledg.on()
        ledy.on()
    if col == "red":
        ledr.on()
    elif col == "green":
        ledg.on()
    else:
        ledy.on()
