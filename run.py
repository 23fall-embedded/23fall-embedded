# -*- coding: utf-8 -*-
#!/usr/bin/python3

from utils.aliyun import aliLink, mqttd
from picamera2 import Picamera2
from decimal import Decimal

import time, json, base64, cv2, shutil, os
import RPi.GPIO as GPIO
import utils.dht11 as dht11
import utils.led as led
import utils.license as license
import utils.ssd3306 as ssd3306
import utils.weather as weather

# import utils.MQ3 as MQ3
import utils.fire as fire
import utils.light as light
import utils.pcf8591 as pcf8591

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

# 三元素（iot后台获取）
ProductKey = "k0kh4u9Sfng"
DeviceName = "pi-1"
DeviceSecret = "7d716841ca95881559e7a8bf7f1ff06c"
# topic (iot后台获取)
POST = "/sys/k0kh4u9Sfng/pi-1/thing/event/property/post"  # 上报消息到云
POST_REPLY = "/sys/k0kh4u9Sfng/pi-1/thing/event/property/post_reply"
SET = "/sys/k0kh4u9Sfng/pi-1/thing/service/property/set"  # 订阅云端指令
user_get = "/k0kh4u9Sfng/pi-1/user/get"
user_update = "/k0kh4u9Sfng/pi-1/user/update"
user_update_err = "/k0kh4u9Sfng/pi-1/user/update/error"
user_send_check = "/k0kh4u9Sfng/pi-1/user/send/check"

cnt = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(17)
weatherNow = weather.checkWeatherNow()
f = fire.fire(24)
l = light.light(26)
led1 = led.led(16, 21, 20)
led2 = led.led(10, 11, 9)
alcohol = 1000
loc = "环翠区"
adm = "威海市"

# 链接信息
Server, ClientId, userName, Password = aliLink.linkiot(
    DeviceName, ProductKey, DeviceSecret
)


# mqtt链接
mqtt = mqttd.MQTT(Server, ClientId, userName, Password)
mqtt.subscribe(SET)  # 订阅服务器下发消息topic
mqtt.subscribe(user_get)
mqtt.subscribe(user_update)
mqtt.subscribe(user_update_err)


picam2 = Picamera2()
picam2.options["quality"] = 50
picam2.options["compress_level"] = 9
picam2.still_configuration.size = (640, 480)

pcf8591.regulate()


# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    print(msg.topic)
    Msg = msg.payload.decode("gbk")
    Msg = json.loads(Msg)

    print(Msg)
    if "alc" in Msg:
        global alcohol
        alcohol = float(Msg["alc"])
    if "loc" in Msg and "adm" in Msg:
        global weatherNow, loc, adm
        loc = Msg["loc"]
        adm = Msg["adm"]
        weatherNow = weather.checkWeatherNow(loc, adm)
    if "led" in Msg:
        col = Msg["led"]
        print(col)
        if col == "off":
            led1.led_off("all")
        else:
            led1.led_on(col)


# 连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass


mqtt.begin(on_message, on_connect)


def get_pic() -> str:
    if not os.path.exists("./img"):
        os.makedirs("./img")
    global cnt
    cnt += 1
    save_path = f"./img/lis_{cnt}.jpg"
    # save_path = "./lis_1.jpg"
    picam2.start(show_preview=True)
    picam2.switch_mode_and_capture_file("still", save_path)
    return save_path


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read())


def clear():
    shutil.rmtree("./img")
    shutil.rmtree("./license")


if os.path.exists("./img"):
    shutil.rmtree("./img")
if os.path.exists("./license"):
    shutil.rmtree("./license")


# 信息获取上报，每5秒钟上报一次系统参数
try:
    while True:
        time.sleep(5)
        result = instance.read()

        temperature = 0
        humidity = 0
        mq3_result = float(
            Decimal(pcf8591.get()).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP")
        )
        fire_result = f.check()
        light_result = l.check()
        code = "1234"

        path = get_pic()
        # print(path)
        num, licenses = license.run(path)

        if fire_result:
            led2.led_on("red")
        else:
            led2.led_off("red")

        if light_result:
            led2.led_on("yellow")
        else:
            led2.led_off("yellow")

        if mq3_result >= alcohol:
            led2.led_on("green")
        else:
            led2.led_off("green")

        print(result.is_valid(), num)

        if True:
            temperature = result.temperature
            humidity = result.humidity
            ssd3306.show(temperature, humidity, licenses, 8)
            if num != 0:
                cur_path = f"./license/lis_{cnt}.jpg"
                # cur_path = "./license/lis_1.jpg"
                code = str(get_base64(cur_path))
            # print(code, type(code))

            # 构建与云端模型一致的消息结构
            updateMsn = {
                "temperature": [temperature],
                "humidity": [humidity],
                "img": [code],
                "mq3": [mq3_result],
                "fire": [fire_result],
                "light": [light_result],
                "licenses": licenses,
            }
            JsonUpdataMsn = aliLink.Alink(updateMsn)
            print(JsonUpdataMsn)

            if cnt % 60 == 0:
                clear()

            mqtt.push(POST, JsonUpdataMsn)  # 定时向阿里云IOT推送我们构建好的Alink协议数据

        ssd3306.show2(
            f"{adm}{loc}天气状况：{weatherNow['text']}，温度：{weatherNow['temp']}°C，体感温度：{weatherNow['feelsLike']}°C，湿度：{weatherNow['humidity']}%，风向风力：{weatherNow['windDir']}{weatherNow['windScale']}级",
            "，",
            9,
        )
except KeyboardInterrupt:
    GPIO.cleanup()
