# Overview
Automation for visualization of benchmark results captured via Java Microbenchmark Harness.
The automation supports 2 file formats:
* **Plain text.** Raw results of JMH printed out in regular, plain text format. Useful in case JMH had been launched from IDE
without any additional options.
* **CSV**. Results of JMH benchmark exported in CSV format.

# Available options

| Option | Short | Type | Description |
| --- | --- | --- | ------------- |
| `directory` | `-d` | `string` | Directory with text files containing JMH results. |
| `percentile` | `-p` | `int` | Target percentile for the visualization. |
| `is_plain_text` | `-i` | `boolean` | If specified, plain text (JMH results) would be parsed, otherwise CSV. |


# Requirements
* Python 3

# Build
```
python3 -m pip install -U pip && python3 -m pip install -U matplotlib
```

# Execute
```
python3 visualize.py -d <source directory> -p <percentile>
```
