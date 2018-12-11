package com.tncet.music;

import java.util.Random;

public class MyCollections
{
    public static Object[] shuffle(Object[] a, Random random) {
        int m = a.length;
        for (int i = m - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            Object tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
        return a;
    }
}
