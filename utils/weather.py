import hashlib
import time
import requests

HEFENG_KEY = "8aa110183dd6419092782f94dbe34e1c"
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


def get_req(url):
    response = requests.get(url)
    return response.json()


def checkWeatherNow(loc="威海", adm="山东"):
    params = {"location": loc, "adm": adm, "t": time.time(), "publicid": PUBLICID}
    url = f"https://geoapi.qweather.com/v2/city/lookup?{encode(params)}"
    message = get_req(url)
    if message["code"] == "200":
        loc = message["location"][0]["id"]
    else:
        raise ValueError("获取 api 失败")
    params = {"location": loc, "t": time.time(), "publicid": PUBLICID}
    code = encode(params)
    url = f"https://devapi.qweather.com/v7/weather/now?{code}"
    message = get_req(url)
    if message["code"] == "200":
        now = message["now"]
        weather = {
            "text": now["text"],
            "temp": now["temp"],
            "feelsLike": now["feelsLike"],
            "humidity": now["humidity"],
            "windDir": now["windDir"],
            "windScale": now["windScale"],
        }
        return weather
    else:
        raise ValueError("获取 api 失败")
