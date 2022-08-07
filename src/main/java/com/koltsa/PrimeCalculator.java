// Moved to package to simplify execution
package com.koltsa;

import benchmark.jmh.CalculatorBenchmark;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import java.util.stream.Stream;

// What is the purpose of this class?
class BigIntegerIterator {
    private final List<String> contain = new ArrayList<>(500);
    private final List<Integer> reference = new ArrayList<>(500);

    BigIntegerIterator(int i) {
        contain.add("" + i + "");
        reference.add(i);
    }

    Integer getContain() {
        return Math.max(Integer.decode(contain.get(0)),reference.get(0));
    }
}

public class PrimeCalculator {
    public static void main(String[] args) throws InterruptedException, IOException, RunnerException {
        System.out.println(PrimeCalculatorSieveOfEratosthenes.getPrimes(Integer.parseInt(args[0])));
//        ThreadSupportTest.checkHowManyThreadsJvmCouldHave();
//        Options opt = new OptionsBuilder()
//                // -- benchmark that'd be ran
//                .include(CalculatorBenchmark.class.getSimpleName() + ".*")
//                .warmupIterations(1)
//                .mode(Mode.SampleTime)
//                .forks(1)
//                .build();
//
//        new Runner(opt).run();

//        PrimeCalculatorEnhanced.getPrimes(Integer.parseInt(args[0]));
//        System.out.println(PrimeCalculator.getPrimes(Integer.parseInt(args[0])));
//        CalculatorBenchmark benchmark = new CalculatorBenchmark();
//        benchmark.init();
        return;
//        for (Integer prime : getPrimes(Integer.parseInt(args[0]))) {
//            System.out.println(prime);
//        }
    }

    // changed 'private' to 'public' static
    public static List<Integer> getPrimes(int maxPrime) throws InterruptedException {
        List<Integer> primeNumbers = Collections.synchronizedList(new LinkedList<>());
        List<BigIntegerIterator> myFiller = Stream.generate(new Supplier<BigIntegerIterator>() {
            int i = 2;

            // Redundant code - could be replaced with a simple loop
            @Override
            public BigIntegerIterator get() {
                return new BigIntegerIterator(i++);
            }
        }).limit(maxPrime).collect(Collectors.toList());

        for (BigIntegerIterator integer : myFiller) {
            primeNumbers.add(integer.getContain());
        }

        List<Integer> primeNumbersToRemove = Collections.synchronizedList(new LinkedList<>());
        CountDownLatch latch = new CountDownLatch(maxPrime);
        ExecutorService executors = Executors.newFixedThreadPool(Math.max(maxPrime / 100, 3000));

        // amount of threads had been changed due to system limitations: 3000 -> 1500 (inability to create native thread)
        // 'synchronized' does not guarantee there won't be a deadlock. Essentially, it makes this part logically single-threaded , ...
        // ... thus, given 3000+ threads, the program will hang.
        synchronized (primeNumbersToRemove) {
            for (Integer candidate : primeNumbers) {
                executors.submit(() -> {
                    try {
                        isPrime(primeNumbers, candidate);
                    } catch (Exception e) {
                        primeNumbersToRemove.add(candidate);
                    }
                    latch.countDown();
                });
            }
        }
        latch.await();
        executors.shutdownNow();
        for (Integer toRemove : primeNumbersToRemove) {
            primeNumbers.remove(toRemove);
        }

        return primeNumbers;
    }

    private static void isPrime(List<Integer> primeNumbers, Integer candidate) throws Exception {
        for (Integer j : primeNumbers.subList(0, candidate - 2)) {
            if (candidate % j == 0) {
                throw new Exception();
            }
        }
    }
}
