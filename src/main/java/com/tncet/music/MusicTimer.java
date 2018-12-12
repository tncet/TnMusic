package com.tncet.music;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.util.Calendar;
import java.util.Date;
import java.util.Properties;
import java.util.Random;
import java.util.Timer;

import javazoom.jl.player.Player;


public class MusicTimer
{
    Timer timer;
    // 播放分钟数
    Long timeSpan = 20L;
    // 播放时间点
    Date broadTime = new Date();

    //时间间隔
    private static final long PERIOD_DAY = 24 * 60 * 60 * 1000;

    public MusicTimer() {

    }

    public void Start() {
        if (broadTime.before(new Date())) {
            broadTime = this.addDay(broadTime, 1);
        }
        timer = new Timer();
        MusicTask task = new MusicTask(this.timeSpan);
        System.out.println("----任务准备执行---- " + "schedule: " + this.broadTime.toString());
        System.out.println("设置播放时长："+this.timeSpan.toString()+"分钟");
        timer.schedule(task, broadTime, PERIOD_DAY);
    }

    public Date addDay(Date date, int num) {
        Calendar startDT = Calendar.getInstance();
        startDT.setTime(date);
        startDT.add(Calendar.DAY_OF_MONTH, num);
        return startDT.getTime();
    }

    public void setBroadTime(int hour, int min, int sec) {
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.HOUR_OF_DAY, hour);
        calendar.set(Calendar.MINUTE, min);
        calendar.set(Calendar.SECOND, sec);
        this.broadTime = calendar.getTime();

    }

    public void setBroadTime(String dateStr) {
        String[] tmp = dateStr.split(":");
        if (tmp.length < 3) {
            System.out.println("时间配置错误"+dateStr);
            System.exit(1);
        }
        Calendar calendar = Calendar.getInstance();
        calendar.set(Calendar.HOUR_OF_DAY, Integer.parseInt(tmp[0]));
        calendar.set(Calendar.MINUTE, Integer.parseInt(tmp[1]));
        calendar.set(Calendar.SECOND, Integer.parseInt(tmp[2]));
        this.broadTime = calendar.getTime();
    }

    public static void main( String[] args ) throws Exception
    {
        Long timeSpan = 20L;

        Properties prop = new Properties();
        FileInputStream in = new FileInputStream("db.properties");
        prop.load(in);
        try {
            timeSpan = Long.parseLong(prop.getProperty("timeSpan"));
            String lunchTime = prop.getProperty("lunch");
            String dinnerTime = prop.getProperty("dinner");
            // 设置午饭计时任务
            MusicTimer lunch = new MusicTimer();
            lunch.timeSpan = timeSpan;
            // lunch.setBroadTime(9,17,0);
            lunch.setBroadTime(lunchTime);
            lunch.Start();
    
            // 设置晚饭计时任务
            MusicTimer dinner = new MusicTimer();
            dinner.timeSpan = timeSpan;
            dinner.setBroadTime(dinnerTime);
            // dinner.setBroadTime(17,30,0);
            dinner.Start();
        } catch (Exception ex) {
            System.out.println(ex.getStackTrace());
        }
        
        
    }
}
