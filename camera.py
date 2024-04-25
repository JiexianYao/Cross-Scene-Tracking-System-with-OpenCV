# 本文件存储摄像头和图像帧读取相关操作
# This file include functions of camera and frame reading
import cv2
import numpy as np
from detector import Detector
import tracker
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QMenuBar,
QSizePolicy, QStatusBar, QWidget)


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
    # 蓝 色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝 polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)
    # 黄 色盘
    yellow_color_plate = [0, 255, 255]
    # 黄 polygon图片
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
    detector = Detector()
    capture = cv2.VideoCapture()
    capture2 = cv2.VideoCapture()

    pix1:cv2.Mat
    
    # 开启摄像头开始监控
    def startMonitoring(self):
        self.capture2 = cv2.VideoCapture(0)
        self.capture = cv2.VideoCapture(1)
        self.timer.timeout.connect(self.turnOnCamera)
        self.timer.start(50)

    # 退出程序结束监控
    def stopMonitoring(self):
        self.capture2.release()
        self.capture.release()
        QApplication.quit()
        print("程序已结束！")
    


    
    # 打开摄像头的函数
    def turnOnCamera(self):
        # 开启摄像头读取视频帧，并将其更新到QLabel上
        # 读取每帧图片
            _,im = self.capture.read()
            _,im2 = self.capture2.read()
            # 缩小尺寸，1920x1080->960x540
            im = cv2.resize(im, (960, 540))
            im2 = cv2.resize(im2, (960, 540))
            list_bboxs = []
            bboxes = self.detector.detect(im)
            # 如果画面中 有bbox
            if len(bboxes) > 0:
                list_bboxs = tracker.update(bboxes, im)
                # 画框
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
                pass
            else:
                # 如果画面中 没有bbox
                output_image_frame = im
            pass
            # 输出图片
            output_image_frame = cv2.add(output_image_frame, self.color_polygons_image)
            if len(list_bboxs) > 0:
                # ----------------------判断撞线----------------------
                for item_bbox in list_bboxs:
                    x1, y1, x2, y2, _, track_id = item_bbox

                    # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                    y1_offset = int(y1 + ((y2 - y1) * 0.6))

                    # 撞线的点
                    y = y1_offset
                    x = x1

                    if self.polygon_mask_blue_and_yellow[y, x] == 1:
                        # 如果撞 蓝polygon
                        if track_id not in self.list_overlapping_blue_polygon:
                            self.list_overlapping_blue_polygon.append(track_id)
                        pass

                        # 判断 黄polygon list 里是否有此 track_id
                        # 有此 track_id，则 认为是 外出方向
                        if track_id in self.list_overlapping_yellow_polygon:
                            # 外出+1
                            up_count += 1

                            print('up count:', up_count, ', up id:', self.list_overlapping_yellow_polygon)

                            # 删除 黄polygon list 中的此id
                            self.list_overlapping_yellow_polygon.remove(track_id)

                            pass
                        else:
                            # 无此 track_id，不做其他操作
                            pass

                    elif self.polygon_mask_blue_and_yellow[y, x] == 2:
                        # 如果撞 黄polygon
                        if track_id not in self.list_overlapping_yellow_polygon:
                            self.list_overlapping_yellow_polygon.append(track_id)
                        pass

                        # 判断 蓝polygon list 里是否有此 track_id
                        # 有此 track_id，则 认为是 进入方向
                        if track_id in self.list_overlapping_blue_polygon:
                            # 进入+1
                            down_count += 1
                            print('down count:', down_count, ', down id:', self.list_overlapping_blue_polygon)
                            # 删除 蓝polygon list 中的此id
                            self.list_overlapping_blue_polygon.remove(track_id)
                            pass
                        else:
                            # 无此 track_id，不做其他操作
                            pass
                        pass
                    else:
                        pass
                    pass

                pass

            # ----------------------清除无用id----------------------
                list_overlapping_all = self.list_overlapping_yellow_polygon + self.list_overlapping_blue_polygon
                for id1 in list_overlapping_all:
                    is_found = False
                    for _, _, _, _, _, bbox_id in list_bboxs:
                        if bbox_id == id1:
                            is_found = True
                            break
                        pass
                    pass

                    if not is_found:
                        # 如果没找到，删除id
                        if id1 in self.list_overlapping_yellow_polygon:
                            self.list_overlapping_yellow_polygon.remove(id1)
                        pass
                        if id1 in self.list_overlapping_blue_polygon:
                            self.list_overlapping_blue_polygon.remove(id1)
                        pass
                    pass
                list_overlapping_all.clear()
                pass

                # 清空list
                list_bboxs.clear()

                pass
            else:
                # 如果图像中没有任何的bbox，则清空list
                self.list_overlapping_blue_polygon.clear()
                self.list_overlapping_yellow_polygon.clear()
                pass
            pass

            text_draw = 'DOWN: ' + str(self.down_count) + \
                    ' , UP: ' + str(self.up_count)
            output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                            org=self.draw_text_postion,
                                            fontFace=self.font_draw_number,
                                            fontScale=1, color=(255, 255, 255), thickness=2)
            output_image_frame = cv2.cvtColor(output_image_frame, cv2.COLOR_BGR2RGB)
            im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)
            pixmap1 = QImage (output_image_frame, 960, 540, QImage.Format_RGB888)
            pixmap1 = QPixmap.fromImage(pixmap1)
            pixmap2 = QImage (im2, 960, 540, QImage.Format_RGB888)
            pixmap2 = QPixmap.fromImage(pixmap2)
            self.label.setPixmap(pixmap1)
            self.label_2.setPixmap(pixmap2)
            self.pix1 = im2
            #print("程序运行时间",time.perf_counter())

