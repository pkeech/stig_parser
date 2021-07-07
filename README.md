<p align="center">
  <img src="docs/images/STIG_Parser.png" />
</p>

[![PyTest Scan](https://github.com/pkeech/stig_parser/actions/workflows/pytest-package.yml/badge.svg)](https://github.com/pkeech/stig_parser/actions) [![PyPI](https://img.shields.io/pypi/v/stig-parser)](https://pypi.org/project/stig-parser/)
### About
A basic Python package to parse DISA STIG (XCCDF) Files into a readable JSON format.

### Installation
To install stig-parser, simple run the following command:

`pip install stig-parser`

### Version Updates
The table below briefly describes each update. For more information, view the releases page.

| Version | Description |
| :---: | --- | 
| 1.0.0 | Initial Creation of **stig-parser** |
| 1.0.1 | Updated to handle change to STIG schema ([Issue #3](https://github.com/pkeech/stig_parser/issues/3)) |
| 1.0.2 | Added Additional Fields to Output JSON. View Release Notes for Full Details ([Issue #9](https://github.com/pkeech/stig_parser/issues/9))|

### Documentation

Documentation hasn't been created at this time. For the current development documentation, please visit the [repository](https://github.com/pkeech/stig_parser).

### Testing 
This project leverages GitHub Actions for its CI/CD workflow. During a Push to any branch, with the exception of `Master` and `Dev`, the workflow will perform Unit Testing and Linting.

For manual testing, run the following commands;

``` bash
## START PYTHON DEV CONTAINER
docker run -it --rm -v $(PWD)/dev:/testing python /bin/bash

## INSTALL DEPENDENCIES
pip install pytest

## RUN PYTEST
pytest
```

### Usage

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

### Output

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


### Dependencies

The following packages are required for this package:

| Package Name | Reason |
| :---: | --- |
| xmltodict | This converts the raw XML file to a python dictionary for ease of processing |

### Comments, Concerns and Gripes

If you have any comments, concerns and/or gripes, please feel free to submit an issue on the [repository](https://github.com/pkeech/stig_parser).
