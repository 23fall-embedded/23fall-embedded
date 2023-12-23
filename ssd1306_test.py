from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

font_ch = ImageFont.truetype("platech.ttf", 12)


def show(temp, humi, licenses):
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")  # 让屏幕周围显示一个框
        draw.text(
            (10, 10), f"温度：{temp}°C，湿度：{humi}%", fill="white", font=font_ch
        )  # col, line
        cnt = 0
        for license in licenses:
            draw.text((10, 22 + (cnt * 12)), license, fill="white", font=font_ch)
        sleep(2)
