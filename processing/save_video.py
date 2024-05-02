import cv2
import time
import threading
from core.camera import camera


# class save_video_thread(threading.Thread):

#     def saveVideo(self): # 保存摄像头后5秒的视频
#         fourcc = cv2.VideoWriter_fourcc(*'MJPG')  #用于保存视频编码的四字参数
#         result = cv2.VideoWriter("tmp_data/savedVideo.avi", fourcc, 1, (960,480)) #保存录像带文件格式
#         print("现在开始录制视频！")
        
#         # 假设 camera.tmp_im2 是你捕获的图像，这里简化处理
        
#         # 每秒记录24帧，因此我们需要计算每一帧之间的时间间隔
#         frame_interval = 1
        
#         # 记录开始时间
#         start_time = time.perf_counter()
        
#         # 每帧的时间戳
#         frame_time = start_time
        
#         # 视频保存成功标志
#         success = False
        
#         while True:
#             # 假设 camera.tmp_im2 是你捕获的图像，这里简化处理
#             # 将图像保存到视频中
#             result.write(self.tmp_im2)
#             print("记录1帧")
#             # 等待下一帧
#             time.sleep(frame_interval)
            
#             # 更新下一帧的时间戳
#             frame_time += frame_interval
            
#             # 检查是否录制结束
#             if frame_time >= start_time + 15:  # 后5秒
#                 success = True
#                 cv2.imwrite("tmp_data/video_test.jpg",camera.tmp_im2)
#                 break

#         if success:
#             print("视频保存成功！")
#         else:
#             print("视频保存失败！")




class SaveVideoThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.frame_interval = 1 / 24
        self.start_time = time.perf_counter()
        self.success = False
        self.lock = threading.Lock()  # 创建锁对象

    def run(self):
        print("现在开始录制视频！")
        frame_time = self.start_time
        
        while True:
            with self.lock:
                # 假设 camera.tmp_im2 是你捕获的图像，这里简化处理
                camera.result.write(camera.tmp_im2)
                print("记录1帧")
            time.sleep(self.frame_interval)
            frame_time += self.frame_interval
            
            # 检查是否录制结束
            if frame_time >= self.start_time + 5:  # 后5秒
                self.success = True
                cv2.imwrite("tmp_data/video_test.jpg", camera.tmp_im2)
                camera.result.release()
                break

        if self.success:
            print("视频保存成功！")
        else:
            print("视频保存失败！")

def video_record():
    # 创建线程并启动
    print(camera.tmp_im2)
    save_video_thread = SaveVideoThread()
    save_video_thread.start()
