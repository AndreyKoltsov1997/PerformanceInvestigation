package benchmark.jmh;

import com.koltsa.PrimeCalculator;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

public class CalculatorBenchmark {

    @Benchmark
    @BenchmarkMode(Mode.SampleTime)
    public void init() {
        // Do nothing
    }

    @State(Scope.Benchmark)
    public static class ExecutionPlan {

        @Param({ "100", "1000", "10000", "100000" })
        public int iterations;
    }

    @Fork(value = 1, warmups = 1)
    @Benchmark
    @BenchmarkMode(Mode.SampleTime)
    public void runOriginalImplementation(BenchmarkBase.ExecutionPlan plan) throws InterruptedException {
        PrimeCalculator.getPrimes(Integer.parseInt(String.valueOf(plan.iterations)));
    }


    public void benchmarkOriginalSolution() throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(CalculatorBenchmark.class.getSimpleName())
                .forks(1)
                .build();

        new Runner(opt).run();
    }
}
