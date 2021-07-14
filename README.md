<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/pkeech/stig_parser">
    <img src="docs/images/STIG_Parser.png" alt="Logo" />
  </a>

  <p align="center">
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/pkeech/stig_parser/issues">Report Bug</a>
    ·
    <a href="https://github.com/pkeech/stig_parser/issues">Request Feature</a>
  </p>
</p>

<!-- PROJECT SHIELDS -->
![GitHub last commit][commit-shield]
[![PyPi][pypi-shield]][pypi-url]
[![GitHub Workflow Status][workflow-shield]][workflow-url]
[![GitHub Open Issues][issues-shield]][issues-url]
[![GitHub Open PRs][pr-shield]][pr-url]
![Python Versions][python-version-shield]
[![GitHub License][license-shield]][license-url]
[![LinkedIN Profile][linkedin-shield]][linkedin-url]

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

### Testing (Unit Testing)
This project leverages GitHub Actions for its CI/CD workflow. During a Push to any branch, with the exception of `Master` and `Dev`, the workflow will perform Unit Testing and Linting.

For manual testing, run the following commands;

``` bash
## START PYTHON DEV CONTAINER
docker run -it --rm -v $(PWD)/dev:/testing python /bin/bash

## INSTALL DEPENDENCIES
pip install pytest

## CHANGE WORKING DIRECTORY
cd testing

## RUN PYTEST
pytest
```

### Testing (Functional Testing)
To perform a functional test, run the following commands. This script will generate a `dump.json` file within the `dev` directory that can be reviewed for accuracy.

``` bash
## START PYTHON DEV CONTAINER
docker run -it --rm -v $(PWD)/dev:/testing python /bin/bash

## INSTALL DEPENDENCIES
pip install stig-parser

## CHANGE WORKING DIRECTORY
cd testing

## RUN PYTHON SCRIPT
python3 test.py
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
    "title": "xxxxxxx",
    "description": "xxxxxxx",
    "version": "x",
    "release": "x ",
    "benchmark_date": "xxxxxxx",
    "release_info": "xxxxxxx",
    "source": "xxxxxxx",
    "notice": "xxxxxxx",
    "rules": [
        {
            "id": "xxxxxxx",
            "stig_id": "xxxxxxx",
            "severity": "xxxxxxx",
            "title": "xxxxxxx",
            "description": "xxxxxxx",
            "fixtext": "xxxxxxx",
            "check": "xxxxxxx",
            "cci": "xxxxxxx",
            "rule_id": "xxxxxxx"
        },
        {
            "id": "xxxxxxx",
            "stig_id": "xxxxxxx",
            "severity": "xxxxxxx",
            "title": "xxxxxxx",
            "description": "xxxxxxx",
            "fixtext": "xxxxxxx",
            "check": "xxxxxxx",
            "cci": "xxxxxxx",
            "rule_id": "xxxxxxx"
        }
    ]
}
```


### Dependencies
The following packages are required for this package:

| Package Name | Reason |
| :---: | --- |
| xmltodict | This converts the raw XML file to a python dictionary for ease of processing |

### Comments, Concerns and Gripes
If you have any comments, concerns and/or gripes, please feel free to submit an issue on the [repository](https://github.com/pkeech/stig_parser).

<!-- MARKDOWN LINKS & IMAGES -->
[commit-shield]: https://img.shields.io/github/last-commit/pkeech/stig_parser?style=for-the-badge
[pypi-shield]: https://img.shields.io/pypi/v/stig-parser?style=for-the-badge
[pypi-url]: https://pypi.org/project/stig-parser/
[workflow-shield]: https://img.shields.io/github/workflow/status/pkeech/stig_parser/Build%20&%20Deploy%20PyPi%20Package?style=for-the-badge
[workflow-url]: https://github.com/pkeech/stig_parser/actions
<!-- [workflow-test-shield]: https://img.shields.io/github/workflow/status/pkeech/stig_parser/integration-dev?label=BUILD%20%28DEV%29&style=for-the-badge -->
<!-- [workflow-test-url]: https://github.com/pkeech/stig_parser/actions -->
[issues-shield]: https://img.shields.io/github/issues/pkeech/stig_parser?style=for-the-badge
[issues-url]: https://github.com/pkeech/stig_parser/issues
[pr-shield]: https://img.shields.io/github/issues-pr/pkeech/stig_parser?style=for-the-badge
[pr-url]: https://github.com/pkeech/stig_parser/pulls
[python-version-shield]: https://img.shields.io/pypi/pyversions/stig-parser?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/pkeech/stig_parser?style=for-the-badge
[license-url]: https://github.com/pkeech/stig_parser/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/peter-keech-b88183a2/