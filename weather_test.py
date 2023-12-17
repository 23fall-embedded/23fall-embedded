import hashlib
import time
import requests

import utils.ssd3306 as ssd3306

HEFENG_KEY = "8aa110183dd6419092782f94dbe34e1c"
LOCATION = "122.06,37.53"
PUBLICID = "HE2312171657561523"

def encode(params):
    params = sorted(params.items(), key=lambda x: x[0], reverse=False)
    params = dict(params)
    string = ""
    if "publicid" not in params.keys() or "t" not in params.keys():
        raise TypeError("缺少必须的参数 publicid 和 t")
    for k, v in params.items():
        if v == "" or k == "sign":
            continue
        else:
            string = string + f"{k}={v}&"
    cur = string
    string = cur[:-1] + HEFENG_KEY
    return f"{cur}sign={hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()}"

def test():
    while True:
        params = {
            "location": LOCATION,
            "t": time.time(),
            "publicid": PUBLICID
        }
        code = encode(params)
        url = f"https://devapi.qweather.com/v7/weather/now?{code}"
        print(url)
        response = requests.get(url)
        message = response.json()

        if message["code"] == "200":
            now = message["now"]
            ssd3306.show2(f"现在天气状况：{now['text']}，温度：{now['temp']}°C，体感温度：{now['feelsLike']}°C，湿度：{now['humidity']}%，风向风力：{now['windDir']}{now['windScale']}级", "，", 9)
        else:
            raise ValueError("获取 api 失败")
        url = f"https://devapi.qweather.com/v7/weather/3d?{code}"
        response = requests.get(url)
        message = response.json()
        if message["code"] == "200":
            tomorrow = message["daily"][1]
            day2 = message["daily"][2]
            ssd3306.show2(f"明天白天天气状况：{tomorrow['textDay']}，温度：{tomorrow['tempMin']}到{tomorrow['tempMax']}°C，湿度：{tomorrow['humidity']}%，风向风力：{tomorrow['windDirDay']}{tomorrow['windScaleDay']}级", "，", 9)
            ssd3306.show2(f"明天夜间天气状况：{tomorrow['textNight']}，温度：{tomorrow['tempMin']}到{tomorrow['tempMax']}°C，风向风力：{tomorrow['windDirNight']}{tomorrow['windScaleNight']}级", "，", 9)
            ssd3306.show2(f"后天白天天气状况：{day2['textDay']}，温度：{day2['tempMin']}到{day2['tempMax']}°C，湿度：{day2['humidity']}%，风向风力：{day2['windDirDay']}{day2['windScaleDay']}级", "，", 9)
            ssd3306.show2(f"后天夜间天气状况：{day2['textNight']}，温度：{day2['tempMin']}到{day2['tempMax']}°C，风向风力：{day2['windDirNight']}{day2['windScaleNight']}级", "，", 9)
        else:
            raise ValueError("获取 api 失败")

test()