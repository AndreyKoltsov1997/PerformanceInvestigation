package benchmark.jmh;

import com.koltsa.PrimeCalculator;
import com.koltsa.PrimeCalculatorEnhanced;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

import java.util.concurrent.TimeUnit;

@OutputTimeUnit(TimeUnit.MILLISECONDS)
public class CalculatorBenchmark {

    // State objects naturally encapsulate the state on which benchmark is working on.
    // The Scope of state object defines to which extent it is shared among the worker thread
    // Scope.Benchmark because all threads could share this variable. It's read-only
    @State(Scope.Benchmark)
    public static class CalculatorBenchmarkPlan {

        //        @Param({ "1000", "10000", "800000" })
        @Param({"1000", "10000", "50000"})
        public int iterations;
    }

    @Benchmark
    // @Fork - instructs how benchmark execution will happen. 'value' controls how many times the benchmark ...
    // ... will be executed. 'warmups' controls how many times the benchmark will be executed prior to results collection.
    @Fork(value = 1, warmups = 3)
    @BenchmarkMode(Mode.SampleTime)
    public void runOriginalImplementation(CalculatorBenchmarkPlan plan, Blackhole blackhole) throws InterruptedException {
        blackhole.consume(PrimeCalculator.getPrimes(Integer.parseInt(String.valueOf(plan.iterations))));
    }

    @Benchmark
    // @Fork - instructs how benchmark execution will happen. 'value' controls how many times the benchmark ...
    // ... will be executed. 'warmups' controls how many times the benchmark will be executed prior to results collection.
    @Fork(value = 1, warmups = 3)
    @BenchmarkMode(Mode.SampleTime)
    public void runEnhancedBenchmark(CalculatorBenchmarkPlan plan, Blackhole blackhole) throws InterruptedException {
        blackhole.consume(PrimeCalculatorEnhanced.getPrimes(Integer.parseInt(String.valueOf(plan.iterations))));
    }

}
