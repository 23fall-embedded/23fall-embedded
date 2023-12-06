import time
import RPi.GPIO as GPIO
from .delay_time import delay_micro_sec


class DHT11Result:
    "DHT11 sensor result returned by DHT11.read() method"

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR


class DHT11:
    "DHT11 sensor reader class for Raspberry"
    __pin = 0

    def __init__(self, pin):
        self.__pin = pin

    def read(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        # send initial high
        self.__send_and_sleep(GPIO.HIGH, 10 * 1000)
        # pull down to low
        self.__send_and_sleep(GPIO.LOW, 25 * 1000)
        # change GPIO port to input
        GPIO.output(self.__pin, GPIO.HIGH)
        GPIO.setup(self.__pin, GPIO.IN)

        # collect data
        data = self.__collect_input()

        # if bit count mismatch, return error(4bytes data + 1byte error)
        if len(data) != 40:
            return DHT11Result(DHT11Result.ERR_MISSING_DATA, 0, 0)

        # trans bits to bytes
        the_bytes = self.__calc_bits(data)

        checksum = the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]

        if the_bytes[4] != checksum:
            return DHT11Result(DHT11Result.ERR_CRC, 0, 0)
        assert the_bytes[4] == checksum

        # The meaning of the return sensor values
        # the_bytes[0]: humidity int
        # the_bytes[1]: humidity decimal
        # the_bytes[2]: temperature int
        # the_bytes[3]: temperature decimal

        temperature = the_bytes[2] + (float(the_bytes[3]) / 10)
        humidity = the_bytes[0] + (float(the_bytes[1]) / 10)

        return DHT11Result(DHT11Result.ERR_NO_ERROR, temperature, humidity)

    def __send_and_sleep(self, output, sleep):
        GPIO.output(self.__pin, output)
        delay_micro_sec(sleep)

    def __collect_input(self):
        cur = []
        self.__wait_init(1)  # get high until low
        self.__wait_init(0)  # get low until high
        self.__wait_init(1)  # get high until low
        # next get data
        for _ in range(40):
            self.__wait_init(0)  # get low until high
            delay_micro_sec(28)  # delay 28us
            if GPIO.input(self.__pin):  # if still high
                cur.append(1)
                self.__wait_init(1)  # get high until low
            else:
                cur.append(0)
        return cur

    def __wait_init(self, st):
        a = time.time()
        while GPIO.input(self.__pin) == st:
            b = time.time()
            if (b - a) > 0.1:
                break

    def __calc_bits(self, bits):
        humidity_bit = bits[0:8]
        humidity_point_bit = bits[8:16]
        temperature_bit = bits[16:24]
        temperature_point_bit = bits[24:32]
        check_bit = bits[32:40]

        humidity_int = 0
        humidity_point = 0
        temperature_int = 0
        temperature_point = 0
        check = 0

        for i in range(8):
            humidity_int += humidity_bit[i] * 2 ** (7 - i)
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
            temperature_int += temperature_bit[i] * 2 ** (7 - i)
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
            check += check_bit[i] * 2 ** (7 - i)

        return [humidity_int, humidity_point, temperature_int, temperature_point, check]


# sudo vi /home/dusker/.local/lib/python3.11/site-packages/dht11/__init__.py
