from collections import defaultdict
import matplotlib.pyplot as plt
import locale
import os


"""
Describes single measurement from JMH.
"""
class BenchmarkMeasurement:
    def __init__(self, group_name, sample_size, percentile, value, measurement):
        self.group_name = group_name
        self.sample_size = int(sample_size)
        self.percentile = percentile
        # value.replace
        self.value = float(value.replace(',', ''))
        # Operations per second, operations per nanosecond, etc.
        self.measurement = measurement

def __get_payload_from_line(group: str, line: str) -> BenchmarkMeasurement:
    """
    Example of line: ...
    # CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95                      1000  sample             1,217             ms/op
    :param group: - test name
    :param line: - raw output of JMH
    """
    payload = line.split()
    # 5 - minimal amount of elements within valuable payload
    if len(payload) < 5:
        return None

    # We'd want percentiles below 100th. I don't split by special symbols since they're different on Windows and macOS, thus might ...
    # ... be OS-dependent. 
    percentile = payload[0].split('p0.')[1] if 'p0' in payload[0] else None
    return BenchmarkMeasurement(group_name=group, sample_size=payload[1], percentile=f"{percentile}th", value=payload[3], measurement=payload[4])

def __get_samples(sample_size: str, percentile: str, object: list) -> list:
    final_list = list(filter(lambda measure: measure.sample_size == sample_size and measure.percentile == percentile, object))
    print(f"len(final_list) {len(final_list)}")
    result = list(map(lambda x: x.value, final_list))

    print(final_list)
    return result

def __print_data(file_path) -> None:
    # Define data values
    x = [7, 14, 21, 28, 35, 42, 49]
    y = [5, 12, 19, 21, 31, 27, 35]
    z = [3, 5, 11, 20, 15, 29, 31]
    # sample size, percentile, value, group name
    # Sample Size <-> [Objects]
    data = defaultdict(list)

    # TODO: get all files from path
    with open(file_path) as file:
        for line in file:

            jmh_measurement = __get_payload_from_line('test_group', line)
            if not jmh_measurement or jmh_measurement.percentile != '95th':
                continue
            # simplified grouping
            data[jmh_measurement.sample_size].append(jmh_measurement)

    # Plot a simple line chart
    # <sample-duration> for each percentile
    # samples should be constant for all charts, it's only durations that differ

    x_values = set()
    y_values = list()
    for sample_size, jmh_measurements in data.items():
        x_values.add(sample_size)
        for measurement in jmh_measurements:
            # filter by percentiles here
            if measurement.percentile == '95th':
                y_values.append(measurement.value)

    # 1. Sort x values
    # 2. Get y value for each x value
    # 3. print
    x_values = sorted(x_values)
    y_values = []
    for size in x_values:
        y_values.append(data[size][0].value)
    plt.plot(sorted(x_values), y_values, marker='o', label=file_path)

    # Plot another line on the same chart/graph
    # plt.plot(x, z)

    plt.legend(loc='upper center')
    plt.show()


def plot_files() -> None:
    folder = os.fsencode('sources')

    for file in os.listdir(folder):
        # for file in files:
        print(f"file: {file}")
        filepath = "sources/" + file.decode("utf-8")
        __print_data(filepath)
        
# CalculatorBenchmark.runEnhancedBenchmark                                                 1000  sample  57295      0,872 �    0,006  ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.00                      1000  sample             0,514             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.50                      1000  sample             0,825             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.90                      1000  sample             1,028             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95                      1000  sample             1,217             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.99                      1000  sample             1,628             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.999                     1000  sample             2,427             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.9999                    1000  sample            32,187             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p1.00                      1000  sample            33,063             ms/op
# CalculatorBenchmark.runEnhancedBenchmark                                                 5000  sample  27808      1,796 �    0,015  ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.00                      5000  sample             1,251             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.50                      5000  sample             1,724             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.90                      5000  sample             2,066             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95                      5000  sample             2,265             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.99                      5000  sample             3,019             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.999                     5000  sample             6,117             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.9999                    5000  sample            33,765             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p1.00                      5000  sample            34,406             ms/op
# CalculatorBenchmark.runEnhancedBenchmark                                                10000  sample  13807      3,622 �    0,096  ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.00                     10000  sample             2,404             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.50                     10000  sample             3,142             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.90                     10000  sample             3,699             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95                     10000  sample             4,018             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.99                     10000  sample            33,128             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.999                    10000  sample            34,747             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.9999                   10000  sample            35,627             ms/op
# CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p1.00                     10000  sample            35,652             ms/op
# CalculatorBenchmark.runOriginalImplementation

def main():
    plot_files()

if __name__ == "__main__":
    main()