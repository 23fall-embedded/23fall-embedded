#!/usr/bin/python3

from utils.aliyun import aliLink, mqttd, rpi
import time, json
import RPi.GPIO as GPIO
import utils.dht11 as dht11


# 三元素（iot后台获取）
ProductKey = "k0kh4u9Sfng"
DeviceName = "pi-1"
DeviceSecret = "7d716841ca95881559e7a8bf7f1ff06c"
# topic (iot后台获取)
POST = "/sys/k0kh4u9Sfng/pi-1/thing/event/property/post"  # 上报消息到云
POST_REPLY = "/sys/k0kh4u9Sfng/pi-1/thing/event/property/post_reply"
SET = "/sys/k0kh4u9Sfng/pi-1/thing/service/property/set"  # 订阅云端指令

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(17)


# 消息回调（云端下发消息的回调函数）
def on_message(client, userdata, msg):
    # print(msg.payload)
    Msg = json.loads(msg.payload)
    switch = Msg["params"]["PowerLed"]
    rpi.powerLed(switch)
    print(msg.payload)  # 开关值


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
mqtt.begin(on_message, on_connect)


# 信息获取上报，每10秒钟上报一次系统参数
while True:
    time.sleep(2)
    result = instance.read()

    temperature = 0
    humidity = 0
    cpuTemp = float(rpi.getCPUtemperature())

    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity

        # 构建与云端模型一致的消息结构
        updateMsn = {
            "temperature": temperature,
            "humidity": humidity,
            "cpuTemperature": cpuTemp
        }
        JsonUpdataMsn = aliLink.Alink(updateMsn)
        print(JsonUpdataMsn)

        mqtt.push(POST, JsonUpdataMsn)  # 定时向阿里云IOT推送我们构建好的Alink协议数据
