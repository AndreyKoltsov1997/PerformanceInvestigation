package com.koltsa;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PrimeCalculatorEnhanced {

    /**
     * Returns list of prime numbers from range [2; maxPrime]
     * @param maxPrime - upper bound of prime number;
     * @return list of prime numbers;
     * @throws InterruptedException
     */
    public static List<Integer> getPrimes(int maxPrime) throws InterruptedException {
        ExecutorService executors = Executors.newFixedThreadPool(maxPrime);

        // TODO: handle exception when native thread couldn't be created

        ConcurrentLinkedQueue<Integer> primeNumbersQueue = new ConcurrentLinkedQueue<>();
        // "maxprime-2" since we start from 2
        CountDownLatch latch = new CountDownLatch(maxPrime - 2);

        for (int i = 2; i <= maxPrime; i++) {
            // final efficiency requirement
            final int candidate = i;
            // Possible "java.lang.OutOfMemoryError: unable to create new native thread"
            executors.submit(() -> {
                if (isPrime(candidate)) {
                    primeNumbersQueue.add(candidate);
                }
                latch.countDown();
            });
        }

        // wait until all threads are completed
        latch.await();
        // shut down executors
        executors.shutdownNow();
        return Arrays.asList(primeNumbersQueue.toArray(new Integer[0]));
    }


    /**
     * Check if number is a prime number.
     * Prime numbers: 2, 3, 5, 7, 11, ...
     *
     * @param number
     * @return
     */
    private static boolean isPrime(int number) {
        // Check number in bounds of primes and not an even
        if ((number <= 1) || (number % 2 == 0 && number > 2)) {
            return false;
        }

        for (int i = 2; i < number; i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }
}
