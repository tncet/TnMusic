package com.tncet.music;

import javazoom.jl.player.Player;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.util.Date;
import java.util.Random;
import java.util.TimerTask;

public class MusicTask extends TimerTask
{
    private Long timeSpan;

    public MusicTask(Long timeSpan) {
        this.timeSpan = timeSpan;
    }

    @Override
    public void run() {
        Random random = new Random();
        File[] lunchMusicList = new File("music").listFiles();
        Long startTime = System.currentTimeMillis();
        System.out.println("----当次任务开始："+new Date(startTime).toString());
        System.out.println("---播放时长："+timeSpan+"分钟");
        outer:
        while (true) {
            lunchMusicList = (File[])MyCollections.shuffle(new File("music").listFiles(), random);
            for (File tmpFile : lunchMusicList) {
                if (!tmpFile.isFile()) {
                    continue;
                }
                String fileName = tmpFile.getName();
                String suffix = fileName.substring(fileName.lastIndexOf(".") + 1).toLowerCase();
                try {
                    if (suffix.contains("wav")) {
                        System.out.println("当前播放："+fileName);
                        new WavPlay(tmpFile).play();
                    } else {
                        System.out.println("当前播放："+fileName);
                        BufferedInputStream buffer = new BufferedInputStream(new FileInputStream(tmpFile));
                        new Player(buffer).play();
                    }
                    Long current = System.currentTimeMillis();
                    if (current - startTime > timeSpan * 60 * 1000) {
                        break outer;
                    }
                } catch (Exception ex) {
                    System.out.println("warning:"+ex.getMessage());
                }

            }
        }
        System.out.println("---当次任务结束---");
    }


}
