import cv2
import time

class save_video:
    # 以下参数用于保存视频
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  #用于保存视频编码的四字参数
    result = cv2.VideoWriter("tmp_data/output.avi", fourcc, 1, (960,480)) #保存录像带文件格式

    def saveVideo(self): # 保存摄像头1的前5分钟和后5秒的视频
        print("现在开始录制视频！")
        time_point = time.perf_counter()
        while (True):
            print("你好！")
            print(time_point + 5)
            print(time.perf_counter())
            self.result.write(self.pix1)
            if(time.perf_counter() >= time_point + 5):
                break
        print("视频保存成功！")
