# Overview
Automation for visualization of benchmark results captured via Java Microbenchmark Harness.

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
