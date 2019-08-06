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
        while True:
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow = tomorrow.replace(hour=0, minute=1, second=0)
            delta = (tomorrow - datetime.now()).total_seconds()
            restDay = 0
            #通过api接口判断当前日期是否为节假日
            dateStr = datetime.strftime(datetime.now(), "%Y%m%d")
            url = "http://timor.tech/api/holiday/info/" + dateStr
            try:
                res = requests.get(url)
                if 'null' in res.text[-15:]:
                    print("开始执行")
                    restDay = 0
                else:      
                    print (str(result) + " 休息日")
                    time.sleep(delta)
                    restDay = 1
            except:
                print ("无法获取工作日信息，按默认播放")
                restDay = 0

            if restDay == 0:
                m = self.timeSpan + self.minute
                if m >= 60:
                    next_time = datetime.now().replace(hour=self.hour+1, minute=m%60, second=0)
                else:
                    next_time = datetime.now().replace(hour=self.hour, minute=m, second=0)
                next_timef = datetime.now().replace(hour=self.hour, minute=self.minute, second=0)
                start_time = (next_time - datetime.now()).total_seconds()
                now_time = (datetime.now() - next_timef).total_seconds()
                if start_time >= 0 and now_time >= 0:
                #在已经该开始播放时执行musicTask函数
                    self.musicTask()
                start_time = start_time - self.timeSpan*60

                if start_time >= 0:
                    #在还没到开始播放时执行睡眠到开始播放的时间为止
                    time.sleep(start_time)
                    self.musicTask()
                    #print(counter)
                else:
                    print("等待下一天的"+str(self.dir))
                    time.sleep(delta)


if __name__ == "__main__":
    # 早晨
    morning = TaskTimer()
    morning.timeSpan = 20
    morning.hour = 8
    morning.minute = 10
    morning.dir = '01早晨'
    morning.start()
    # morning.musicTask()
    # 中午
    noon = TaskTimer()
    noon.timeSpan = 30
    noon.hour = 11
    noon.minute = 29
    noon.dir = '02中午'
    noon.start()
    # noon.musicTask()

    # 午休结束
    afternoon = TaskTimer()
    afternoon.timeSpan = 15
    afternoon.hour = 13
    afternoon.minute = 30
    afternoon.dir = '03午休结束'
    afternoon.start()

    # 下午茶
    tea = TaskTimer()
    tea.timeSpan = 15
    tea.hour = 15
    tea.minute = 45
    tea.dir = '04下午茶'
    tea.start()

    # 晚餐
    dinner = TaskTimer()
    dinner.timeSpan = 45
    dinner.hour = 18
    dinner.minute = 0
    dinner.dir = '05晚餐'
    dinner.start()

    # 回家
    night = TaskTimer()
    night.timeSpan = 20
    night.hour = 22
    night.minute = 0
    night.dir = '06回家'
    night.start()
    


'''
测试说明：
    1.开始时间在当前时间之后（通过）
    2.开始时间在当前时间之前，结束时间在当前时间之后（通过）
    3.正常结束（通过）
    4.进程退出（通过）（必须正常结束）
    5.连续任务（待测试）
    6.retry测试（待测试）
'''
