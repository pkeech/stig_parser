<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/pkeech/stig_parser">
    <img src="https://github.com/pkeech/stig_parser/blob/master/docs/images/STIG_Parser.png" alt="Logo" />
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

> **NOTE**: As of version 1.1.0, the JSON output fields have been renamed and CamelCased. This was an effort to standardize the variables being used. When using Versions less than 1.1.0, please ensure you update your field names prior to updating. 

### About
A basic Python package to parse DISA STIGs (XCCDF) into a readable JSON format. 

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
| 1.1.0 | Added Additional Fields to Output JSON, Included BETA release of CKL creation and added the ability to parse a STIG directly from the ZIP file. View Release Notes for Full Details |
| 1.1.1 | Resolved Issues Concerning STIG Rules with Multiple CCIs. Credit: @gregelin |

### Documentation
Documentation hasn't been created at this time. For the current development documentation, please visit the [repository](https://github.com/pkeech/stig_parser).

### Testing
This project leverages GitHub Actions for its CI/CD workflow. During a Push to any branch, with the exception of `Master` and `Dev`, the workflow will perform Unit Testing and Linting.

For manual testing, run the following commands;

``` bash
## START PYTHON DEV CONTAINER
docker run -it --rm -v $(PWD):/stig-parser python /bin/bash

## INSTALL DEPENDENCIES
pip install pytest pytest-cov xmltodict

## CHANGE WORKING DIRECTORY
cd stig-parser

## RUN PYTEST
pytest -v

## RUN PYTEST COVERAGE
pytest --cov src
```

### Usage
This module contains the following functions;

| Function | Description | Parameters |
| --- | --- | --- |
| `convert_stig(STIG_FILE)` | This function will extract the STIG from a ZIP archive, and parse the results into a JSON object | `STIG_FILE` == Path to STIG ZIP File |
| `convert_xccdf(STIG_XML)` | This function will parse a raw bytes of a STIG file (XML) and return a JSON object| `STIG_XML` == Bytes object of STIG xccdf.xml File |
| `generate_stig_json(STIG_JSON, EXPORT_PATH)` | This function will write the STIG JSON object to a File | `STIG_JSON` == JSON Object of STIG, `EXPORT_PATH` == Path to create JSON File |
| `generate_ckl(STIGFILE, CHECKLIST_INFO)` | This function will generate an XML Object of a CKL based upon a passed STIG | `STIG_FILE` == Path to STIG ZIP File , `CHECKLIST_INFO` == JSON Object of additional information needed (see below) |
| `generate_ckl_file(CKL, EXPORT_PATH)` | This function will write the CKL XML Object to a File | `CKL` == XML Object of CKL , `EXPORT_PATH` == Path to create CKL File |

When creating a Checklist (CKL), additional information is required. This information is added to the CKL but is required to be defined prior to creation. For an example of usage, please see the examples below.

``` json
{
  "ROLE": "None",
  "ASSET_TYPE": "Computing",
  "HOST_NAME": "Test_Host",
  "HOST_IP": "1.2.3.4",
  "HOST_MAC": "",
  "HOST_FQDN": "test.hostname.dev",
  "TARGET_COMMENT": "",
  "TECH_AREA": "",
  "TARGET_KEY": "3425",
  "WEB_OR_DATABASE": "false",
  "WEB_DB_SITE": "",
  "WEB_DB_INSTANCE": ""
}
```

### Examples
This module has several use cases that will either generate a JSON object of a STIG file, or an XML object of a CKL file.

#### STIGs
To convert a STIG file to a JSON object, you can utilize the following example.

``` python
## LOAD PYTHON MODULE
from stig_parser import convert_stig

## PARSE STIG ZIP FILE
## ASSUMES ZIP FILE IS IN CURRENT WORKING DIRECTORY
json_results = convert_stig('./U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip')
```

Additionally, this example demonstrates how to generate the STIG JSON object from an **xccdf** file.

``` python
## LOAD PYTHON MODULE
from stig_parser import convert_xccdf

## LOAD XML FILE (OPTIONAL)
import os

with open("U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml", "r") as fh:
    raw_file = fh.read()

## PARSE XCCDF(XML) to JSON
json_results = convert_xccdf(raw_file)
```

#### Checklists (CKL)
To generate a CKL from a given STIG, you can utilize the following example;

``` python
## LOAD PYTHON MODULE
from stig_parser import generate_ckl, generate_ckl_file

## DEFINE STIG FILE LOCATION
## ASSUMES ZIP FILE IS IN CURRENT WORKING DIRECTORY
STIG = './U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip'

## DEFINE EXPORT LOCATION
EXPORT = './ myCKL.ckl'

## DEFINE ADDITIONAL CHECKLIST INFORMATION
CHECKLIST_INFO ={
  "ROLE": "None",
  "ASSET_TYPE": "Computing",
  "HOST_NAME": "Test_Host",
  "HOST_IP": "1.2.3.4",
  "HOST_MAC": "",
  "HOST_FQDN": "test.hostname.dev",
  "TARGET_COMMENT": "",
  "TECH_AREA": "",
  "TARGET_KEY": "3425",
  "WEB_OR_DATABASE": "false",
  "WEB_DB_SITE": "",
  "WEB_DB_INSTANCE": ""
}


## GENERATE CKL XML OBJECT
RAW_CKL = generate_ckl(STIG, CHECKLIST_INFO)

## SAVE CHECKLIST TO FILE
generate_ckl_file(RAW_CKL, EXPORT)
```


### Output
Outlined below is the expected JSON output:

``` json
{
  "Title": "xxxxxxx",
  "Description": "xxxxxxx",
  "Version": "x",
  "Release": "x ",
  "BenchmarkDate": "xxxxxxx",
  "ReleaseInfo": "xxxxxxx",
  "Source": "xxxxxxx",
  "Notice": "xxxxxxx",
  "Rules": [
    {
      "VulnID": "xxxxxxx",
      "RuleID": "xxxxxxx",
      "StigID": "xxxxxxx",
      "Severity": "high | medium | low",
      "Cat": "CAT I | CAT II | CAT III",
      "Classification": "",
      "GroupTitle": "xxxxxxx",
      "RuleTitle": "xxxxxxx",
      "Description": "xxxxxxx",
      "VulnDiscussion": "xxxxxxx",
      "FalsePositives": "xxxxxxx",
      "FalseNegatives": "xxxxxxx",
      "Documentable": "xxxxxxx",
      "Mitigations": "xxxxxxx",
      "SeverityOverrideGuidance": "xxxxxxx",
      "PotentialImpacts": "xxxxxxx",
      "ThirdPartyTools": "xxxxxxx",
      "MitigationControl": "xxxxxxx",
      "Responsibility": "xxxxxxx",
      "IAControls": "xxxxxxx",
      "CheckText": "xxxxxxx",
      "FixText": "xxxxxxx",
      "CCI": "xxxxxxx"
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
