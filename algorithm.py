# 因该系统需要演示9种算法，所以将此算法独立出来
import cv2
import numpy as np

class algo_switch:
# 定义去噪/灰度/追踪算法字典，用以保存切换算法的状态
# 初始化算法状态字典
    algorithm_states = {
        "gaussDenoise": False,  # 预处理——高斯去噪
        "meanDenoise": False,   # 预处理——均值去噪
        "mediDenoise": False,   # 预处理——中值去噪
        "greyFloat": False,     # 灰度处理——浮点操作
        "greyInt": False,       # 灰度处理——整型
        "greyMove": False,      # 灰度处理——移位
        "centroid": False,      # 质心追踪算法
        # 添加更多的算法...
    }


    # 将某一种算法状态设置为激活
    def activate_algorithm(self, algorithm_name):
        # 遍历状态字典，将其他所有算法状态置为关闭
        for state_key in self.algorithm_states.keys():
            self.algorithm_states[state_key] = False
        self.algorithm_states[algorithm_name] = True # 将输入的算法状态置为开启
        print(f"{algorithm_name} algorithm is already activated.")

    # 将算法状态设置为非激活
    def deactivate_algorithm(self, algorithm_name):
        self.algorithm_states[algorithm_name] = False
        print(f"{algorithm_name} algorithm is already deactivated.")



# 预处理——去噪类
class filter():
    def hello():
        print("hello!")

# 预处理——灰度图处理类
class grey():
    def float_gray_image_processing(frame, adjustment):
        # 浮点灰度处理
        greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert pixel values to integers
        frame_int = greyFrame.astype(int)
        # Apply brightness adjustment to each pixel
        adjusted_frame_int = frame_int + adjustment
        # Limit pixel values to the range 0-255
        adjusted_frame_int[adjusted_frame_int < 0] = 0
        adjusted_frame_int[adjusted_frame_int > 255] = 255
        # Convert pixel values back to uint8 type
        adjusted_frame = adjusted_frame_int.astype(np.uint8)
        return adjusted_frame
    

    def integer_gray_image_processing(image):
        # 整型灰度处理
        greyFrame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Convert pixel values to integers
        image_int = greyFrame.astype(int)
        # Example processing: Invert the image
        inverted_image_int = 255 - image_int
        # Convert pixel values back to uint8 type
        inverted_image = inverted_image_int.astype(np.uint8)
        return inverted_image


    def move_gray_image_processing(image, factor):
        # 将图像数据类型转换为int16
        image_int16 = image.astype(np.int16)
        # 应用对比度调整
        adjusted_image_int16 = image_int16 * factor
        # 将超出范围的像素值限制在0-255之间
        adjusted_image_int16[adjusted_image_int16 < 0] = 0
        adjusted_image_int16[adjusted_image_int16 > 255] = 255
        # 将图像数据类型转换回uint8
        adjusted_image = adjusted_image_int16.astype(np.uint8)
        return adjusted_image


# 追踪算法的实现类
class trakcingImplement():
    # 质心追踪算法
    def centroid(frame): # 输入一个帧
        # 转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 使用阈值分割（参数可以根据实际情况调整）
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        # 寻找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历每个轮廓
        for contour in contours:
            # 计算轮廓的质心
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # 在图像上标注质心
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
    
    # 相关滤波追踪算法
    def correclation():
        return 0
    
    # 场景锁定算法
    def sceneLock(frame): # 输入帧
        # 读取第一帧
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        # Shi-Tomasi 角点检测
        corners = cv2.goodFeaturesToTrack(old_gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        # 转换角点数据类型
        corners = np.int0(corners)

        # 转换为灰度图像
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 计算光流
        new_corners, status, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, corners, None)
        # 筛选跟踪成功的角点
        good_new = new_corners[status == 1]
        good_old = corners[status == 1]
        # 计算场景锁定变换矩阵
        M, _ = cv2.estimateAffinePartial2D(good_old, good_new)
        # 应用变换矩阵到原始帧
        result_frame = cv2.warpAffine(old_frame, M, (old_frame.shape[1], old_frame.shape[0]))
        # 更新角点和帧
        corners = cv2.goodFeaturesToTrack(frame_gray, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        corners = np.int0(corners)
        old_frame = frame.copy()
        old_gray = frame_gray.copy()

