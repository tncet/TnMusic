package com.tncet.music;

import java.io.File;
import java.io.IOException;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.SourceDataLine;

/**
 * WavPlay
 */
public class WavPlay {

    private File file;
    private int BUFFER_SIZE = 128000;

    public WavPlay(File file) {
        this.file = file;
    }

    public void play() throws Exception {
        AudioInputStream audioStream = AudioSystem.getAudioInputStream(file);
        AudioFormat audioFormat = audioStream.getFormat();

        DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);

        SourceDataLine sourceLine = (SourceDataLine) AudioSystem.getLine(info);
        sourceLine.open(audioFormat);
        sourceLine.start();

        int nBytesRead = 0;
        byte[] abData = new byte[BUFFER_SIZE];
        while (nBytesRead != -1) {
            try {
                nBytesRead = audioStream.read(abData, 0, abData.length);
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (nBytesRead >= 0) {
                @SuppressWarnings("unused")
                int nBytesWritten = sourceLine.write(abData, 0, nBytesRead);
            }
        }

        sourceLine.drain();
        sourceLine.close();
    }
}