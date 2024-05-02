import cv2
import time
from core.camera import camera
class save_video:

    def saveVideo(): # 保存摄像头后5秒的视频
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  #用于保存视频编码的四字参数
        result = cv2.VideoWriter("tmp_data/savedVideo.avi", fourcc, 1, (960,480)) #保存录像带文件格式
        print("现在开始录制视频！")
        
        # 假设 camera.tmp_im2 是你捕获的图像，这里简化处理
        
        # 每秒记录24帧，因此我们需要计算每一帧之间的时间间隔
        frame_interval = 1
        
        # 记录开始时间
        start_time = time.perf_counter()
        
        # 每帧的时间戳
        frame_time = start_time
        
        # 视频保存成功标志
        success = False
        
        while True:
            # 假设 camera.tmp_im2 是你捕获的图像，这里简化处理
            # 将图像保存到视频中
            result.write(camera.tmp_im2)
            print("记录1帧")
            # 等待下一帧
            time.sleep(frame_interval)
            
            # 更新下一帧的时间戳
            frame_time += frame_interval
            
            # 检查是否录制结束
            if frame_time >= start_time + 15:  # 后5秒
                success = True
                cv2.imwrite("tmp_data/video_test.jpg",camera.tmp_im2)
                break

        if success:
            print("视频保存成功！")
        else:
            print("视频保存失败！")
