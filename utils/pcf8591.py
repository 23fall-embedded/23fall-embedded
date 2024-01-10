import smbus

R0 = 0
RL = 200

address = 0x48
bus = smbus.SMBus(1)

VOLT = 3300


def get_average(t):
    tot = 0
    for _ in range(t):
        tot += bus.read_byte(address)
    return tot / t


def regulate():
    value = get_average(10)
    v = (value * VOLT) / 255
    v = v / 1000
    global R0
    R0 = (((VOLT / 1000) / v) - 1) * RL


def get():
    value = get_average(10)
    v = (value * VOLT) / 255
    v = v / 1000
    Rs = (((VOLT / 1000) / v) - 1) * RL
    final = 0.4 * pow(Rs / R0, -1.5)
    return max(0.00, final - 0.4)
