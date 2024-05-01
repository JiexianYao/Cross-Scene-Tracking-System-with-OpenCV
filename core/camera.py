# 本文件存储摄像头和图像帧读取相关操作
# This file include functions of camera and frame reading
import cv2
import numpy as np
from processing import detector
import processing.tracker as tracker
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QMenuBar,
QSizePolicy, QStatusBar, QWidget)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from processing import algorithm
from . import ui_setup

class camera():
    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
    # 初始化2个撞线polygon
    list_pts_blue = [[0, 0]]
    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=1)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]
    # 填充第二个polygon
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)
    list_pts_yellow = [[0, 0]]
    ndarray_pts_yellow = np.array(list_pts_yellow, np.int32)
    polygon_yellow_value_2 = cv2.fillPoly(mask_image_temp, [ndarray_pts_yellow], color=2)
    polygon_yellow_value_2 = polygon_yellow_value_2[:, :, np.newaxis]
    # 撞线检测用mask，包含2个polygon，（值范围 0、1、2），供撞线计算使用
    polygon_mask_blue_and_yellow = polygon_blue_value_1 + polygon_yellow_value_2
    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue_and_yellow = cv2.resize(polygon_mask_blue_and_yellow, (960, 540))
    # 蓝色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)
    # 黄色盘
    yellow_color_plate = [0, 255, 255]
    # 黄polygon图片
    yellow_image = np.array(polygon_yellow_value_2 * yellow_color_plate, np.uint8)

    # RGB颜色空间（值范围 0-255）
    color_polygons_image = blue_image + yellow_image
    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (960, 540))
    # list与蓝色polygon重叠
    list_overlapping_blue_polygon = []
    # list与黄色polygon重叠
    list_overlapping_yellow_polygon = []
    # 进入数量
    down_count = 0
    # 离开数量
    up_count = 0
    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))



    # 初始化高斯混合模型
    detector = detector.Detector()
    # 声明opencv摄像头捕捉对象
    capture = cv2.VideoCapture(1)
    capture2 = cv2.VideoCapture(0)

    img1:np
    img2:np
   