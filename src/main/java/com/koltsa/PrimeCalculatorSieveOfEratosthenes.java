package com.koltsa;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

/**
 * Implements determination of prime numbers using Sieve of Eratosthenes algorithm.
 * Details: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
 */
public class PrimeCalculatorSieveOfEratosthenes {

    /**
     * Determines prime numbers from range [2; maxPrime].
     *
     * @param maxPrime - upper bound of target prime number sequence.
     * @return list of prime numbers from range [2; maxPrime].
     */
    public static List<Integer> getPrimes(final int maxPrime) {
        // Create a "table" of numbers [2; maxPrime] and mark all of them as 'true'.
        boolean[] tableOfNums = new boolean[maxPrime + 1];
        Arrays.fill(tableOfNums, true);

        // Linked List, since we always append at the end => O(1) time complexity
        List<Integer> primeNumbers = new LinkedList();
        for (int number = 2; number <= maxPrime; number++) {
            if (!tableOfNums[number]) {
                continue;
            }
            primeNumbers.add(number);
            // -- iterate over multipliers of numbers, e.g.: [2, 4, 6, 8, ...]
            for (int multiplier = number * 2; multiplier <= maxPrime; multiplier += number) {
                // -- mark all multipliers of prime number as composite
                tableOfNums[multiplier] = false;
            }
        }
        return primeNumbers;
    }
}
