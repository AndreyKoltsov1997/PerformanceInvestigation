package com.koltsa.utilities;

public class ThreadCountTest {

    private static int threadCount = 0;

    /**
     * Checks how many threads current JVM supports by sequentially spawning the threads and ...
     * ... printing out their number into standard output.
     */
    public static void checkHowManyThreadsJvmCouldHave() {
        Object monitor = new Object();
        for (;;) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    synchronized (monitor) {
                        ThreadCountTest.threadCount++;
                        System.out.println(String.format("Thread count: %d", ThreadCountTest.threadCount++));
                    }
                    for (;;) {
                        // hold thread in active state
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }).start();
        }
    }
}
