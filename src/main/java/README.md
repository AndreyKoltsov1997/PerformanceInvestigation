# Issues

1. isPrime(...) signature is insufficient. It could be replaces with boolean rather than throwing and handlng excewption.

# Profiling
YourTrack had been used via Intellij IDEA. The IntelliJ's run method had been excluded from profiling.


# Experiment 1 - increase
Value changed: 100 -> 100000 in order to increase amount of samples collected.
As a result - Java OOM. Do we need to create that many threads? (certainly not)
It's such an expensive operation.
Starting from ~5000, on my macbook, I observed inability to create new thread (208 threads). It's abnormal and related to JVM configuration on my macbook,

```
Exception in thread "main" java.lang.OutOfMemoryError: unable to create new native thread
	at java.lang.Thread.$$YJP$$start0(Native Method)
	at java.lang.Thread.start0(Thread.java)
	at java.lang.Thread.start(Thread.java:719)
	at java.util.concurrent.ThreadPoolExecutor.addWorker(ThreadPoolExecutor.java:957)
	at java.util.concurrent.ThreadPoolExecutor.execute(ThreadPoolExecutor.java:1367)
	at java.util.concurrent.AbstractExecutorService.submit(AbstractExecutorService.java:112)
	at PrimeCalculator.getPrimes(PrimeCalculator.java:55)
	at PrimeCalculator.main(PrimeCalculator.java:29)
Error occurred during initialization of VM
java.lang.OutOfMemoryError: unable to create new native thread

Process finished with exit code 1
```
![img.png](img.png)

Abnormal due ot amount of threads mac could handle
``` 
% sysctl kern.num_threads
kern.num_threads: 10240
```

```
andreykoltsov@Andreys-MacBook-Air ~ % ulimit -a
-t: cpu time (seconds)              unlimited
-f: file size (blocks)              unlimited
-d: data seg size (kbytes)          unlimited
-s: stack size (kbytes)             8176
-c: core file size (blocks)         0
-v: address space (kbytes)          unlimited
-l: locked-in-memory size (kbytes)  unlimited
-u: processes                       1333
-n: file descriptors                2560

```



As a result, experiment had been run with custom JVM options in order to increase heap size.

![img_2.png](img_2.png)

# 1. Default implementation
* Argument: 500000 (for sufficient sample size)
* JVM options: `-XX:+UnlockDiagnosticVMOptions -XX:+PrintFlagsFinal -Xmx4000m` (otherwise Java OOM)
* Thread liimt: amount of threads had been changed due to system limitations: 3000 -> 1500 (inability to create native thread), 
## 1.1 CPU analysis (Code had been modified to use fixed amount of threads) - general

![img_3.png](img_3.png)
A more simple view would be in the form of flamegraph:
![img_5.png](img_5.png)
Found issues:
* Issue 1. The sampling matches part of the code responsible for the removal of the available prime numbers. They're stored within `LinkedList` - an insufficient collection for such case, since each removal require traversing, which is implemented via O(N) lookup time. A more sufficient collection would be HashMap, since it provides O(1) lookup time.
* Issue 2 & 3. Both of them are related to insufficient control of application flow. Depending on stack trace, stack depth and its type, the creation of `Exception` instance is expensive. In an environment where they're constantly created in order to control the application flow, the affection on performance (CPU, Heap and, as a result, GC) is inevitable. As an alternative, we should replace the signature to use `boolean` variable.

## 1.2 Heap analysis
Heap usage is insufficient for such application.
![img_4.png](img_4.png)

## 1.3 Potential deadlock

Potential deadlock (probably thread is frozen due to GC activity and not an actual deadlock)
![img_1.png](img_1.png)