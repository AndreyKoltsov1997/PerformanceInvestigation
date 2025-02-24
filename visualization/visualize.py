import os, sys, getopt
from argparse import ArgumentError
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv

"""
Describes single measurement from JMH.
"""
class BenchmarkMeasurement:
    def __init__(self, sample_size: str, percentile: str, value: str, measurement: str):
        self.sample_size = int(sample_size)
        self.percentile = percentile
        # -- JMH prints results as "0,124", "1,123" and all of them are integer. ...
        # ... I haven't found a locale option that'd handle it without errors, thus replacing ...
        # ... it manually.
        self.value = float(value.replace(',', '.'))
        # Operations per second, operations per nanosecond, etc.
        self.measurement = measurement


def __get_jmh_measurement_from_csv_line(csv_elements: list) -> BenchmarkMeasurement:
    """
    Retrieves JMH Measurement from its results provided as a CSV file.
    Example of CSV Element: ...
    ... "Benchmark","Mode","Threads","Samples","Score","Score Error (99,9%)","Unit","Param: maxPrimeNumber"
    :param csv_elements: - line of CSV file read by CSV reader
    :returns: BenchmarkMeasurement instance
    """
    if len(csv_elements) < 5:
        return None

    # We'd want percentiles below 100th. I don't split by special symbols since they're different on Windows and macOS, thus might ...
    # ... be OS-dependent. 
    percentile = csv_elements[0].split('p0.')[1] if 'p0' in csv_elements[0] else None
    return BenchmarkMeasurement(sample_size=csv_elements[7], percentile=f"{percentile}th", value=csv_elements[4], measurement=csv_elements[6])


def __get_jmh_measurement_from_line(line: str) -> BenchmarkMeasurement:
    """
    Retrieves JMH Measurement from its results provided as a plain text.
    Example of line: ...
    # CalculatorBenchmark.runEnhancedBenchmark:runEnhancedBenchmark�p0.95   1000  sample   1,217   ms/op
    :param group: - test name
    :param line: - raw output of JMH
    :returns: BenchmarkMeasurement instance
    """
    payload = line.split()
    
    # 5 - minimal amount of elements within valuable payload
    if len(payload) < 5:
        return None

    # We'd want percentiles below 100th. I don't split by special symbols since they're different on Windows and macOS, thus might ...
    # ... be OS-dependent. 
    percentile = payload[0].split('p0.')[1] if 'p0' in payload[0] else None
    return BenchmarkMeasurement(sample_size=payload[1], percentile=f"{percentile}th", value=payload[3], measurement=payload[4])


def __get_jmh_measurement_matching_criteria(measurements: list[BenchmarkMeasurement], sample_size: int, percentile: str) -> BenchmarkMeasurement:
    """
    Retrieves JMH measurement based on provided criterias.
    :param measurements: - list of JMH measurements
    :param sample_size: - JMH sample size used within measurement
    :param percentile: - percentile of JMH result
    """
    samples = list(filter(lambda measure: (measure.percentile == percentile and measure.sample_size == sample_size), measurements))
    if (len(samples) > 1):
        # unexpected - JMH uses unique percentiles
        raise ValueError(f"Found more than 1 sample for given percentile: {percentile}")
    return samples[0]


def __get_jmh_measurements_from_reader_object(reader_obj: object, is_csv: bool):
    """
    Retrieves JMH measurement from reader object.
    :param reader_obj: - source for data, it might be plain text iterator, CSV file iterator, etc.
    :param is_csv: - indicates if source file has CSV format
    """
    data = defaultdict(list)

    for line in reader_obj:
        try:
            jmh_measurement = (__get_jmh_measurement_from_csv_line(line) 
                                if is_csv 
                                else __get_jmh_measurement_from_line(line))
        except Exception as e:
            print(f"Unable to parse line: {line} \n {e}")
            continue
        
        if not jmh_measurement:
            continue
        data[jmh_measurement.sample_size].append(jmh_measurement)

    return data


def __get_plottable_jmh_data_from_csv_file(file_path: str) -> dict:
    """
    Retrieves JMH measurements in a plottable format from CSV file.
    :param file_path: - path to file with measurements
    :returns: dictionary: <sample size> - <[measurements]
    """
    data = defaultdict(list)
    with open(file_path) as file:
        reader_obj = csv.reader(file)
        data = __get_jmh_measurements_from_reader_object(reader_obj=reader_obj, is_csv=True)
    return data


def __get_plottable_jmh_data_from_plain_text_file(file_path: str) -> dict:
    """
    Retrieves JMH measurements in a plottable format from plain text file.
    :param file_path: - path to file with measurements
    :returns: dictionary: <sample size> - <[measurements]
    """
    data = defaultdict(list)
    with open(file_path) as file:
        data = __get_jmh_measurements_from_reader_object(reader_obj=file, is_csv=False)
    return data


def plot_jmh_measurements(datasource_path: str, percentile: int, is_plain_text: bool = False) -> None:
    """
    1. Parses files from given folders and retrieves JMH measurements.
    2. Plots measurements based on parsed data.
    :param datasource_path: - path to folder where JMH measurements are locatedl
    :param percentile: - target percentile
    """
    folder = os.fsencode(datasource_path)

    # -- Get data
    fname_with_plottable_data = defaultdict()
    for file in os.listdir(folder):
        filename_decoded = file.decode('utf-8')
        filepath = f"{datasource_path}/{filename_decoded}"
        fname_with_plottable_data[filename_decoded] = (__get_plottable_jmh_data_from_plain_text_file(filepath) 
                                                        if is_plain_text 
                                                        else __get_plottable_jmh_data_from_csv_file(filepath))
    
    # -- Visualize Data
    fig, ax = plt.subplots()
    ax.ticklabel_format(useOffset=False)
    for filename, sample_size_to_jmh_data in fname_with_plottable_data.items():
        x_values = sorted(sample_size_to_jmh_data.keys())
        y_values = list()
        for size in x_values:
            # -- get certain percentile for given sample size
            measurement = __get_jmh_measurement_matching_criteria(sample_size_to_jmh_data[size], size, f"{percentile}th")
            y_values.append(measurement.value)
        ax.plot(sorted(x_values), y_values, marker='o', label=filename)

    plt.title(f"Java Microbenchmark Harness, {percentile}th percentile")
    plt.xlabel('Max Prime Number')
    plt.ylabel('Duration, ms/op')
    plt.legend(loc='upper left')
    
    # Set log scale that'd print actual values instead of power of 10s. Note that ...
    # ... the order is important - ticket should format axis after log scale is set.
    plt.yscale('log')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
    plt.show()


def main(argv):
    try:
        # -- parse CLI options
        opts, args = getopt.getopt(argv, 'hd:p:i:', ['directory=', 'percentile=', 'is_plain_text='])
        print(opts)
        if not opts:
            raise getopt.GetoptError('Not enough arguments.')
    except (getopt.GetoptError, ArgumentError) as e:
        print(f"{e} \n Usage: python3 visualize.py -d <source directory> -p <percentile>")
        sys.exit(2)
    
    # -- actions based on CLI options
    usage = 'python3 visualize.py -d <source directory> -p <percentile> -u <(optional> parse plain text>'
    source_directory = ''
    target_percentile = ''
    should_parse_plain_txt = False
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-p':
            target_percentile = arg
        elif opt == '-d':
            source_directory = arg
        elif opt == '-i':
            # plain text specified
            should_parse_plain_txt = True

    
    # -- print 95th percentile by default
    target_percentile = int(target_percentile) if target_percentile else 95
    if not source_directory:
        raise ValueError(f"Source directory not specified. \n {usage}")
    plot_jmh_measurements(source_directory, target_percentile, should_parse_plain_txt)


if __name__ == "__main__":
   main(sys.argv[1:])
