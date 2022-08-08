# Overview
![img_17.png](../documentation/comparison-chart-enhancements-of-code.png)

Automated visualization of performance test results conducted via [Java Microbenchmark Harness (JMH)](https://github.com/openjdk/jmh).

The automation supports 2 file formats:
* **Plain text.** Raw results of JMH printed out in regular, plain text format. Mostly useful in case JMH had been launched via IDE.
* **CSV**. Results of JMH benchmark exported in CSV format.

# Available options

| Option | Short | Type | Description |
| --- | --- | --- | ------------- |
| `directory` | `-d` | `string` | Directory with text files containing JMH results. |
| `percentile` | `-p` | `int` | Target percentile for the visualization. |
| `is_plain_text` | `-i` | `boolean` | If specified, plain text (JMH results) would be parsed, otherwise CSV. |


# Requirements
* Python 3.6.0+

# Build
```
python3 -m pip install -U pip && python3 -m pip install -U matplotlib
```

# Execute
```
python3 visualize.py -d <source directory> -p <percentile>
```
