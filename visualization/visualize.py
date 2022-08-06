import os, sys, getopt
from argparse import ArgumentError
from collections import defaultdict
import matplotlib.pyplot as plt


"""
Describes single measurement from JMH.
"""
class BenchmarkMeasurement:
    def __init__(self, sample_size, percentile, value, measurement):
        self.sample_size = int(sample_size)
        self.percentile = percentile
        # -- JMH prints results as "0,124", "1,123" and all of them are integer. ...
        # ... I haven't found a locale option that'd handle it without errors, thus repliacing ...
        # ... it manually.
        self.value = float(value.replace(',', ''))
        # Operations per second, operations per nanosecond, etc.
        self.measurement = measurement


def __get_payload_from_line(line: str) -> BenchmarkMeasurement:
    """
    Example of line: ...
    # CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95   1000  sample   1,217   ms/op
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
    return BenchmarkMeasurement(sample_size=payload[1], percentile=f"{percentile}th", value=payload[3], measurement=payload[4])


def __get_samples(sample_size: str, percentile: str, object: list) -> list:
    final_list = list(filter(lambda measure: measure.sample_size == sample_size and measure.percentile == percentile, object))
    result = list(map(lambda x: x.value, final_list))
    return result



def __get_data_as_dict(file_path) -> dict:
    # sample size, percentile, value, group name
    # Sample Size <-> [Objects]
    data = defaultdict(list)

    with open(file_path) as file:
        for line in file:
            try:
                jmh_measurement = __get_payload_from_line(line)
            except Exception as e:
                print(f"Unable to parse line: {line} \n {e}")
                continue
            
            if not jmh_measurement or jmh_measurement.percentile != '95th':
                continue
            data[jmh_measurement.sample_size].append(jmh_measurement)
    return data


def __print_data(file_path) -> None:
    # sample size, percentile, value, group name
    # Sample Size <-> [Objects]
    data = defaultdict(list)

    with open(file_path) as file:
        for line in file:
            try:
                jmh_measurement = __get_payload_from_line(line)
            except Exception as e:
                print(f"Unable to parse line: {line} \n {e}")
                continue
            
            if not jmh_measurement or jmh_measurement.percentile != '95th':
                continue
            data[jmh_measurement.sample_size].append(jmh_measurement)

    # Plot a simple line chart
    # <sample-duration> for each percentile
    # samples should be constant for all charts, it's only durations that differ

    x_values = set()
    y_values = list()
    for sample_size, jmh_measurements in data.items():
        x_values.add(sample_size)

    # 1. Sort x values
    # 2. Get y value for each x value
    # 3. print
    x_values = sorted(x_values)
    y_values = []
    for size in x_values:
        y_values.append(data[size][0].value)
    plt.plot(sorted(x_values), y_values, marker='o', label=file_path)


def plot_files_via_dict(datasource_path: str) -> None:
    folder = os.fsencode(datasource_path)

    plottable_data = defaultdict()
    for file in os.listdir(folder):
        filename_decoded = file.decode('utf-8')
        filepath = f"{datasource_path}/{filename_decoded}"
        plottable_data[filename_decoded] = __get_data_as_dict(filepath)
    
    # visualize
    for filename, jmh_measurements in plottable_data.items():
        x_values = list(jmh_measurements.keys())
        y_values = list()

        # 1. Sort x values
        # 2. Get y value for each x value
        # 3. print
        x_values = sorted(x_values)
        y_values = []
        for size in x_values:
            y_values.append(jmh_measurements[size][0].value)
        plt.plot(sorted(x_values), y_values, marker='o', label=filename)


    plt.xlabel('Sample size')
    plt.ylabel('Score, ms/op')
    plt.legend(loc='upper center')
    plt.show()

def plot_files(datasource_path: str) -> None:
    folder = os.fsencode(datasource_path)

    for file in os.listdir(folder):
        filepath = f"{datasource_path}/" + file.decode('utf-8')
        __print_data(filepath)

    plt.xlabel('Sample size')
    plt.ylabel('Score, ms/op')
    plt.legend(loc='upper center')
    plt.show()


def main(argv):
    try:
        # -- parse CLI options
        opts, args = getopt.getopt(argv, 'hd:', ['dir='])
        print(opts)
        if not opts:
            raise getopt.GetoptError('Not enough arguments.')
    except (getopt.GetoptError, ArgumentError) as e:
      print(f"{e} \n Usage: python3 visualize.py -d <source directory>")
      sys.exit(2)
    
    # -- actions based on CLI options
    for opt, arg in opts:
        if opt == '-d':
            plot_files_via_dict(arg)
            sys.exit(0)


if __name__ == "__main__":
   main(sys.argv[1:])
