#coding:utf-8

import multiprocessing
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
        self.timeSpan = 20
        self.hour = 8
        self.minute = 10
        self.dir = '01早晨'

    def chooseMusicFile(self, files: list):
        if len(files) > 0:
            file = files.pop(0)
            files.append(file)
            return file
        else:
            return ''

    def musicTask(self):
        dateStr = datetime.strftime(datetime.now(), "%Y%m%d")
        url = "http://tool.bitefu.net/jiari/?d=" + dateStr
        try:
            res = requests.get(url)
            if res.text != "0":
                print (res + " 休息日")
                return
        except:
            print ("无法获取工作日信息，按默认播放")
        
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
        startTime = datetime.now().replace(
            hour=self.hour, minute=self.minute, second=0)
        endTime = startTime + timedelta(minutes=self.timeSpan)
        path = os.path.join(os.path.abspath('.'), self.dir)
        # if platform.system() == 'Windows':
        #     path = os.path.abspath('.') + '/' + self.dir
        files = [
            item for item in os.listdir(path)
            if not (os.path.isdir(item) or item.startswith('.'))
        ]
        random.shuffle(files)
        print ('本次播放任务任务: ' + self.dir)
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
                #mixer.music方法
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
        scheduler = BlockingScheduler()
        scheduler.add_job(
            self.musicTask,
            'cron',
            day_of_week='0-6',
            hour=self.hour,
            minute=self.minute)
        print (self.dir + ' 任务启动')
        scheduler.start()
        


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

    morning.join()
    noon.join()
    afternoon.join()
    tea.join()
    dinner.join()
    night.join()