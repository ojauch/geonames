# Geonames Python Library

Simple python library to access the [Geonames](https://www.geonames.org/) REST API

## Usage

```
usage: geonames.py [-h] --username USERNAME (--json | --csv) [input] [output]

Get geo information for a list of places from Geonames

positional arguments:
  input                 input file (default: stdin)
  output                output file (default: stdout)

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        username to access geonames API
  --json                format output as JSON
  --csv                 format output as CSV
```