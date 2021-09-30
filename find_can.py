import cv2
import numpy as np
def find_can_image(HSV_upper, image):
    ###########################################################
    # img = cv2.imread("D:/python workplace/embedded_final/sprint_x1/x8.jpg")#读取存储路径
    img = image
    height, width = img.shape[:2]
    # 图片缩小两倍，方便显示
    reSize1 = cv2.resize(img, (int(width/2), int(height/2)), interpolation=cv2.INTER_CUBIC)
    #########################################################################
    # 做一个投影， 得到的图片为了满足不畸变，变为h，w = 420， 540
    points1 = np.float32([[210, 120], [750, 120], [0, 540], [960, 540]])
    points2 = np.float32([[0,0], [540,0], [0,420], [540,420]])

    # 计算得到转换矩阵
    M = cv2.getPerspectiveTransform(points1, points2)

    # 实现透视变换转换
    processed = cv2.warpPerspective(reSize1, M, (540,420))
    #########################################################################
    imgContour =processed.copy()
    lower = np.array([0,0,0])
    upper = np.array(HSV_upper)
    imgHSV = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)  #要处理的图像转换成HSV
    mask = cv2.inRange(imgHSV,lower, upper) #把img和mask做and操作，使得图片二值化
    imgMask = cv2.bitwise_and(processed,processed,mask=mask)
    # cnt = imgMask
    imgblur1 = cv2.GaussianBlur(mask,(5,5),10,10)      #高斯滤波，边缘平滑（查）
    kernel1 = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(imgblur1,kernel1,iterations=5)

    # binary, contours, hierarchy = cv2.findContours(erosion, mode=cv2.RETR_EXTERNAL,
    #                                            method=cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(erosion, mode=cv2.RETR_EXTERNAL,
                                               method=cv2.CHAIN_APPROX_NONE)
    for cn in contours:
        M = cv2.moments(cn)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])  # 计算质心. 建系，图像h方向表示y，w方向表示x
            cY = int(M["m01"] / M["m00"])
            cv2.circle(imgContour, (cX, cY), 7, (255, 0, 255), -1)
            cv2.putText(imgContour, "can", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # cv2.imshow("imgmask",cnt)
            cv2.imshow("goood",imgContour)
    cv2.waitKey(0)
    return cX, cY


def cal_actual_distance(can_x, can_y, pixel_x=900, pixel_y=1000):
    # 在本函数中，基坐标系是图片bottom边的中点，一切都需要转换到该坐标系下，注意，y轴指向后方
    car_x = 0.0 * pixel_x    # 车子先做转向
    car_y = -0.2 * pixel_y       # 目前认为进去5cm易拉罐肯定可以捡到了，再加上自身车长15cm
    # 对can_x和can_y进行处理，放置到该坐标系下
    can_x = 270 - can_x
    can_y = 420 - can_y
    actual_x = (can_x - car_x) / pixel_x
    actual_y = (can_y - car_y) / pixel_y
    return actual_x, actual_y
