import time


def delay_micro_sec(t):  # 微秒级延时函数
    start, end = 0, 0  # 声明变量
    start = time.time()  # 记录开始时间
    t = (t - 3) / 1000000  # 将输入t的单位转换为秒，-3是时间补偿
    while end - start < t:  # 循环至时间差值大于或等于设定值时
        end = time.time()  # 记录结束时间
