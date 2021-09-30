import cv2
import numpy
import os
import serial
import find_can as fd
import serial_cmd as sc

if __name__ == '__main__':
    # # loogson下使用
    # path = "/home/cjj/uvc/frame.jpg"
    # os.system("cd /home/cjj/uvc;./capture")
    # img = cv2.imread(path)
    # # win下使用
    img = cv2.imread("D:\python workplace\embedded_final\datasets_1/80.jpg")  # 读取存储路径
    # 方便当场调节
    HSV_upper = [40, 255, 255]
    # 串口初始化
    portx = "/dev/ttyUSB0"
    bps = "115200"
    timex = 5
    ser = serial.Serial(portx, bps, timeout=timex)
    cmd_vel = sc.Cmdvel(ser)
    can_x, can_y = fd.find_can_image(HSV_upper, img)  # can_x是距离top的距离，can_y是距离left的距离
    print(can_x, can_y)
    actual_x,actual_y = fd.cal_actual_distance(can_x, can_y)
    print(actual_x, actual_y)
    sc.car_move(cmd_vel, actual_x, actual_y)
