## About

A basic Python package to parse DISA STIG (XCCDF) Files into a readable JSON format.

## Installation

To install stig-parser, simple run the following command:

`pip install stig-parser`

## Version Updates

| Version | Description |
| :---: | --- | 
| 1.0.0 | Initial Creation of `stig-parser` |
| 1.0.1 | Updated to handle change to STIG schema ([Issue #3](/../../issues/3)) |
| 1.0.2 | Added Additional Fields to Output JSON. View Release Notes for Full Details ([Issue #9](/../../issues/9))|

## Documentation

Documentation hasn't been created at this time. For the current development documentation, please visit the [repository](https://github.com/pkeech/stig_parser).

## Testing 
_Placeholder_

## Usage

To use this package simply, import the module and run the `convert-xccdf()` function. This will result in the a JSON String object. 

``` python
## LOAD PYTHON MODULE
from stig_parser import convert_xccdf

## LOAD XML FILE (OPTIONAL)
import os

with open("example.xml", "r") as fh:
    raw_file = fh.read()

## PARSE XCCDF(XML) to JSON
json_results = convert_xccdf(raw_file)

```

## Output

Outlined below is the expected JSON output:

``` json
{
    benchmark_date: "xxxxxxx",
    description: "xxxxxxxx",
    release: "xx",
    rules: [
        {
            "check": "xxxxxxxx", 
            "description": "xxxxxxxxxx", 
            "fixtext": "xxxxxxxxxx", 
            "id": "xxxxxxx", 
            "severity": "xxxxxxxx", 
            "stig_id": "xx-xx-xxxxxx", 
            "title": "xxxxxxxxxxx"
        },
        {
            "check": "xxxxxxxx", 
            "description": "xxxxxxxxxx", 
            "fixtext": "xxxxxxxxxx", 
            "id": "xxxxxxx", 
            "severity": "xxxxxxxx", 
            "stig_id": "xx-xx-xxxxxx", 
            "title": "xxxxxxxxxxx"
        }
    ],
    title: "xxxxxxxxxx",
    version: "xxxxxxxxx"
}
```


## Dependencies

The following packages are required for this package:

| Package Name | Reason |
| :---: | --- |
| xmltodict | This converts the raw XML file to a python dictionary for ease of processing |

## Comments, Concerns and Gripes

If you have any comments, concerns and/or gripes, please feel free to submit an issue on the [repository](https://github.com/pkeech/stig_parser).