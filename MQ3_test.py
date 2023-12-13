import smbus
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(26, GPIO.IN)

while True:
	dout = GPIO.input(26)
	bus = smbus.SMBus(1)
	data = bus.read_i2c_block_data(0x50, 0x00, 2)

	raw_adc = (data[0] & 0x0F) * 256 + data[1]
	concentration = (3.3 / 65535.0) * raw_adc + 0.05
	if dout == 1:
		print("leaked！")
	print("Alcohol Concentration: %.2f mg/L" % concentration)
	time.sleep(1)


