import cv2
import numpy as np
import hyperlpr3 as lpr3
import os

from PIL import ImageFont, ImageDraw, Image


# 标记车牌
def draw_plate_on_image(img, box, text, font):
    x1, y1, x2, y2 = box
    cv2.rectangle(img, (x1, y1), (x2, y2), (139, 139, 102), 2, cv2.LINE_AA)
    cv2.rectangle(img, (x1, y1 - 20), (x2, y1), (139, 139, 102), -1)
    data = Image.fromarray(img)
    draw = ImageDraw.Draw(data)
    draw.text((x1 + 1, y1 - 18), text, (255, 255, 255), font=font)
    res = np.asarray(data)

    return res


font_ch = ImageFont.truetype("platech.ttf", 20, 0)
catcher = lpr3.LicensePlateCatcher(detect_level=lpr3.DETECT_LEVEL_HIGH)

"""
    给定一张图片的路径，识别出其中的车牌
    img: 图片路径
    返回值：图像中车牌个数
"""


def run(img: str):
    if not os.path.exists("./license"):
        os.makedirs("./license")
    image = cv2.imread(img)

    licenses = []

    results = catcher(image)
    for code, confidence, type_idx, box in results:
        # 解析数据并绘制
        licenses.append(code)
        text = f"{code} - {confidence:.2f}"
        image = draw_plate_on_image(image, box, text, font=font_ch)
        # 保存图像
        cv2.imwrite(f"./license/{os.path.basename(img)}", image)
    return len(results), licenses
