##  ===================================
##  ===== STIG PARSER TEST SCRIPT =====
##  ===================================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : 1.0.2
##  Description : PyTest file for STIG-Parser v1.0.2
##  Requirements: PyTest, XmltoDict
##  Testing     : docker run -it --rm -v $(PWD):/stig-parser python /bin/bash
##                cd stig-parser && pip install pytest xmltodict
##                pytest -s

## IMPORT REQUIRED MODULES
import zipfile, os, pytest

## IMPORT STIG-PARSER
from src.stig_parser import convert_xccdf

##  ----------------------------------------
##  ---- STATICALLY SET TEST VARIABLES -----
##  ----------------------------------------

## STIG FILENAME
FILENAME = "tests/resources/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip"

##  -----------------------
##  ---- PYTEST TESTS -----
##  -----------------------

## TEST: ENSURE STIG FILE EXISTS
def test_requirements() -> None:
    ## CHECK FILE EXISTS
    assert os.path.isfile(FILENAME), 'File does not exist: %s' % FILENAME

## TEST: ATTEMPT TO PARSE STIG FILE
def test_parse_stig() -> None:
    ## OPEN XML FILE FROM ZIP FILE AND OBTAIN LIST OF FILES
    z = zipfile.ZipFile(FILENAME)
    files = z.namelist()

    ## FIND MANUAL STIG FILE
    for file in files:
        if file.endswith('_Manual-xccdf.xml'):
            ## HANDLE MACOS
            if not file.startswith('__MACOS'):
                ## DETERMINE FILE NAME
                STIG_FILENAME = file
                break

    ## ENSURE FILE IS FOUND
    assert STIG_FILENAME is not None, 'Manual STIG File was NOT FOUND'

    ## READ STIG FILE
    RAW_FILE = z.read(STIG_FILENAME)

    ## ENSURE FILE READ CORRECTLY
    assert RAW_FILE is not None, 'Unable to Read STIG File (%s)' % STIG_FILENAME

    ## CONVERT RAW STIG TO JSON OBJECT
    STIG_JSON = convert_xccdf(RAW_FILE)

    ## ENSURE STIG WAS PARSED
    assert STIG_JSON is not None, 'Unable to Parse STIG File (%s)' % STIG_FILENAME

    ## VALIDATE KNOWN ENTRIES
    assert STIG_JSON['title'] == "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide", "STIG Title Parsed Incorrectly"    ## STIG TITLE
    assert STIG_JSON['benchmark_date'] == "19 Jul 2019"     ## BENCHMARK DATE
    assert STIG_JSON['rules'][0]['id'] == "V-94863"     ## FIRST RULE ID
    assert STIG_JSON['release_info'] == "Release: 1 Benchmark Date: 19 Jul 2019"    ## RELEASE INFO
    assert STIG_JSON['source'] == "STIG.DOD.MIL"    ## SOURCE
    assert STIG_JSON['notice'] == "terms-of-use"    ## NOTICE
    #assert STIG_JSON['rules'][0]['cci'] == "CCI-000054"    ## FIRST RULE CCI NUMBER
    assert STIG_JSON['rules'][0]['stig_id'] == "DKER-EE-001000"     ## FIRST RULE STIG ID
    assert STIG_JSON['rules'][0]['rule_id'] == "SV-104693r1_rule"   ## FIRST RULE ID