package com.koltsa;

public class ThreadSupportTest {
    private static int threadCount = 0;

    /**
     * Checks how much threads current JVM supports.
     */
    public static void checkHowManyThreadsJvmCouldHave() {
        Object monitor = new Object();
        for (;;) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    synchronized (monitor) {
                        ThreadSupportTest.threadCount++;
                        System.out.println(String.format("Thread count: %d", ThreadSupportTest.threadCount++));
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
