import serial
import binascii
import cv2
class Cmdvel():
    def __init__(self, ser):
        self.ser = ser

    def int2bin16(self, num):
        return (bin(((1 << 16) - 1) & num)[2:]).zfill(16)

    def get_bcc(self, inputStr):
        bcc = 0
        for i in inputStr.split(' '):
            bcc = bcc ^ int(i, 16)
        return f'{bcc:x}'

    def str_to_hex(self, str):
        return ' '.join([hex(ord(c)).replace('0x', '') for c in str])
    def __call__(self, v_x, v_y, v_z):
        v_x *= 1000
        v_x = self.int2bin16(int(v_x))
        v_x_send = str(v_x)
        v_x_send = hex(int(v_x_send, 2))
        v_x_send = v_x_send[2:].zfill(4)
        v_x_high = v_x_send[0:2]
        v_x_low = v_x_send[2:4]
        v_y *= 1000
        v_y = self.int2bin16(int(v_y))
        v_y_send = str(v_y)
        v_y_send = hex(int(v_y_send, 2))
        v_y_send = v_y_send[2:].zfill(4)
        v_y_high = v_y_send[0:2]
        v_y_low = v_y_send[2:4]
        v_z *= 1000
        v_z = self.int2bin16(int(v_z))
        v_z_send = str(v_z)
        v_z_send = hex(int(v_z_send, 2))
        v_z_send = v_z_send[2:].zfill(4)
        v_z_high = v_z_send[0:2]
        v_z_low = v_z_send[2:4]
        bcc_list = ['7B', '00', '00', v_x_high, v_x_low, v_y_high, v_y_low, v_z_high, v_z_low]
        bcc_input = ' '.join(bcc_list)
        bcc = self.get_bcc(bcc_input)
        print("start")
        self.ser.write(chr(0x7B).encode("utf-8"))
        self.ser.write(chr(0x00).encode("utf-8"))
        self.ser.write(chr(0x00).encode("utf-8"))
        self.ser.write(bytes.fromhex(v_x_high))
        self.ser.write(bytes.fromhex(v_x_low))
        self.ser.write(bytes.fromhex(v_y_high))
        self.ser.write(bytes.fromhex(v_y_low))
        self.ser.write(bytes.fromhex(v_z_high))
        self.ser.write(bytes.fromhex(v_z_low))
        self.ser.write(bytes.fromhex(bcc))
        self.ser.write(chr(0x7D).encode("utf-8"))
        print("end")
        return


def car_move(cmd_vel, actual_x, actual_y, vel=0.15):
    cmd_vel(0, 0, 0.5)
    cv2.waitKey(3100)   #原地旋转90度
    cmd_vel(0, 0, 0)
    cv2.waitKey(1000)
    if actual_x < 0:
        cmd_vel(-vel, 0, 0)
    else:
        cmd_vel(vel, 0, 0)
    time_x = abs(actual_x / vel)
    cv2.waitKey(time_x)
    cmd_vel(0, 0, 0)
    cv2.waitKey(1000)
    cmd_vel(0, -vel, 0)
    time_y = abs(actual_y / vel)
    cv2.waitKey(time_y)
    cmd_vel(0, 0, 0)
    cv2.waitKey(1000)


# portx = "COM5"
# bps = "115200"
# timex = 5
# ser = serial.Serial(portx, bps, timeout=timex)
# # try:
# #     while True:
# #         ser1 = ser.read(8).hex()
# #         print(type(ser1))
# # except:
# #     ser.close()
#
# cmd_vel = Cmdvel(ser)
# cmd_vel(0.1, 0, 0)
#
#
# ser.close()



