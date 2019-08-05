#coding utf-8
'''
Date:2019-08-05
ZYX
日常播放器
'''
import multiprocessing
from retrying import retry
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import pygame
import os
import time
import random
import platform
import requests


class TaskTimer(multiprocessing.Process):
    def __init__(self):
        super(TaskTimer, self).__init__()
        #持续时间
        self.timeSpan = 20
        #播放时间（h）
        self.hour = 17
        #播放时间（m）
        self.minute = 10
        self.dir = '01早晨'
    
    #循环播放
    def chooseMusicFile(self, files: list):
        if len(files) > 0:
            file = files.pop(0)
            files.append(file)
            return file
        else:
            return ''
            
    @retry
    def musicTask(self):
        #初始化混音器
        pygame.mixer.init()
        #设置播放结束事件
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
        #设置播放开始时间 20XX-XX-XX 08:10:00.XXXXXX
        startTime = datetime.now().replace(
            hour=self.hour, minute=self.minute, second=0)
        #设置播放结束时间 20XX-XX-XX 08:30:00.XXXXXX
        endTime = startTime + timedelta(minutes=self.timeSpan)
        #找到播放路径
        path = os.path.join(os.path.abspath('.'), self.dir)
        #if platform.system() == 'Windows':
        #    path = os.path.abspath('.') + '/' + self.dir
        #路径下所有音乐文件
        files = [
            item for item in os.listdir(path)
            if not (os.path.isdir(item) or item.startswith('.'))
        ]
        #随机找到一个文件
        random.shuffle(files)
        print ('本次播放任务: ' + self.dir)
        print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        while True:
            if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > endTime.strftime(
                    '%Y-%m-%d %H:%M:%S'):
                break
            if len(files) == 0:
                # print('当前列表为空，休眠15秒')
                time.sleep(15)
                files = [
                    item for item in os.listdir(path)
                    if not (os.path.isdir(item) or item.startswith('.'))
                ]
                random.shuffle(files)
                continue
            file = self.chooseMusicFile(files)
            if os.path.splitext(file)[-1].lower() in ['.mp3', '.wav', '.flac']:
                # mixer.music方法
                # pygame.mixer.music.load(path + '/' + file)
                pygame.mixer.music.load(os.path.join(path, file))
                # pygame.mixer.music.load(r'C:\Users\Bighansen\tn-music\01早晨\08 爱的喜悦.wav')
                print('开始播放: ' + file)
                pygame.mixer.music.play()
                running = True
                while running:
                    if not pygame.mixer.music.get_busy():
                        running = False
                    else:
                        time.sleep(2)
            elif os.path.splitext(file)[-1].lower() in ['.m4a']:
                time.sleep(2)
                # print (os.path.join(path, file))
                # pygame.mixer.Sound(os.path.join(path, file)).play()
                # print (pygame.mixer.get_busy())
                # running = True
                # while running:
                #     if not pygame.mixer.get_busy():
                #         running = False
                #     else:
                #         time.sleep(2)

        print('本次播放任务结束')
        pygame.quit()

    def run(self):
        #在轮到自己播放时执行musicTask函数
        self.musicTask()


if __name__ == "__main__":
    counter = "01早晨"
    timeList = {
        "01早晨":[8,10,20],
        "02中午":[11,29,30],
        "03午休结束":[13,30,15],
        "04下午茶":[15,45,15],
        "05晚餐":[18,0,45],
        "06回家":[22,0,20]
    }

    while True:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=0, minute=1, second=0)
        delta = (tomorrow - datetime.now()).total_seconds()
        flag = 0
        #判断当前时间是否为0：00-X:XX
        for name,t in timeList.items():
            m = t[1] + t[2]
            next_time = datetime.now().replace(hour=t[0], minute=m, second=0)
            start_time = (next_time - datetime.now()).total_seconds()
            if start_time >= 0:
                print("当前时间"+str(datetime.now())+"， 下次播放时间"+ \
                    str(datetime.now().replace(hour=t[0], minute=t[1], second=0))+ \
                        ", 开始等待")
                #创建进程
                process = TaskTimer() 
                process.timeSpan = t[2]
                process.hour = t[0]
                process.minute = t[1]
                process.dir = name
                counter = name
                flag = 1
                break
        
        start_time = start_time - timeList[counter][2]*60
        #print(start_time)
        if flag == 1:
            if start_time >= 0:
                time.sleep(start_time)
            #print(counter)
            #通过api接口判断当前日期是否为节假日
            dateStr = datetime.strftime(datetime.now(), "%Y%m%d")
            url = "http://tool.bitefu.net/jiari/?d=" + dateStr
            try:
                res = requests.get(url)
                result = res.text.replace('"','')
                result = int(result)
                if result != 0:
                    print (str(result) + " 休息日")
                    time.sleep(delta)
                else:      
                    print("开始执行")
                    process.start()
                    process.join()
            except:
                print ("无法获取工作日信息，按默认播放")
                process.start()
                process.join
        else:
            print("已下班，等待下一天")
            time.sleep(3600)

'''
测试说明：
    1.开始时间在当前时间之后（通过）
    2.开始时间在当前时间之前，结束时间在当前时间之后（通过）
    3.正常结束（通过）
    4.进程退出（通过）（必须正常结束）
    5.连续任务（待测试）
    6.retry测试（待测试）
'''