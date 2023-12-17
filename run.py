#!/usr/bin/python3

from utils.aliyun import aliLink, mqttd, rpi
from picamera2 import Picamera2

import time, json, base64, cv2, shutil, os
import RPi.GPIO as GPIO
import utils.dht11 as dht11
import utils.led as led
import utils.license as license
import utils.ssd3306 as ssd3306

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

cnt = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(17)


# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    print(msg.payload)
    # Msg = msg.payload.decode('utf-8')
    Msg = json.loads(msg.payload)
    print(Msg)
    if "led" in Msg:
        col = Msg["led"]
        print(col)
        if col == "off":
            led.led_off()
        else:
            led.led_on(col)


# 连接回调（与阿里云建立链接后的回调函数）
def on_connect(client, userdata, flags, rc):
    pass


# 链接信息
Server, ClientId, userNmae, Password = aliLink.linkiot(
    DeviceName, ProductKey, DeviceSecret
)

# mqtt链接
mqtt = mqttd.MQTT(Server, ClientId, userNmae, Password)
mqtt.subscribe(SET)  # 订阅服务器下发消息topic
mqtt.subscribe(user_get)
mqtt.subscribe(user_update)
mqtt.subscribe(user_update_err)
mqtt.begin(on_message, on_connect)


def get_pic() -> str:
    if not os.path.exists("./img"):
        os.makedirs("./img")
    # picam2 = Picamera2()
    global cnt
    cnt += 1
    save_path = f"./img/lis_{cnt}.jpg"
    if cnt % 3 == 0:
        img = cv2.imread("./lis_1.jpg")
    elif cnt % 3 == 1:
        img = cv2.imread("./2.jpg")
    else:
        img = cv2.imread("./3.jpg")
    cv2.imwrite(save_path, img)
    return save_path
    # picam2.start_and_capture_file(save_path)
    # return save_path


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read())


def clear():
    shutil.rmtree("./img")
    shutil.rmtree("./license")


# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(2)
    result = instance.read()

    temperature = 0
    humidity = 0
    cpuTemp = float(rpi.getCPUtemperature())

    path = get_pic()
    # print(path)
    num, licenses = license.run(path)
    # print(num, licenses)

    if result.is_valid() and num != 0:
        temperature = result.temperature
        humidity = result.humidity
        cur_path = f"./license/lis_{cnt}.jpg"
        ssd3306.show(temperature, humidity, licenses, 8)
        code = get_base64(cur_path)
        # print(code)

        # 构建与云端模型一致的消息结构
        updateMsn = {
            "temperature": temperature,
            "humidity": humidity,
            "cpuTemperature": cpuTemp,
            # "img": code
        }
        JsonUpdataMsn = aliLink.Alink(updateMsn)
        print(JsonUpdataMsn)

        if cnt % 60 == 0:
            clear()

        mqtt.push(POST, JsonUpdataMsn)  # 定时向阿里云IOT推送我们构建好的Alink协议数据

