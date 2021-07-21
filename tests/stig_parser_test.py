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
import zipfile, os, json, xmltodict, pytest

## IMPORT STIG-PARSER
import src.stig_parser as stig_parser

##  ----------------------------------------
##  ---- STATICALLY SET TEST VARIABLES -----
##  ----------------------------------------

## STIG FILENAME
FILENAME = "tests/resources/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip"

## EXPORT PATHS
EXPORT_PATH_JSON = './tests/pytest-stig.json'
EXPORT_PATH_CKL = './tests/pytest-stig.ckl'
 
## CHECKLIST METADATA
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

##  -----------------------------
##  ----- PRIVATE FUNCTIONS -----
##  -----------------------------

## FUNCTION: CONVERT CHECKLIST (XML) TO DICTIONARY
def convert_ckl_to_dict(RAW_CKL):
    ## CONVERT XML TO PYTHON DICTIONARY
    CHECKLIST_DICT = xmltodict.parse(RAW_CKL, dict_constructor=dict)

    ## RETURN DICTIONARY
    return CHECKLIST_DICT

##  -----------------
##  ----- TESTS -----
##  -----------------

## TEST: ENSURE STIG FILE EXISTS
## REQUIRES: N/A
def test_requirements() -> None:
    ## CHECK FILE EXISTS
    assert os.path.isfile(FILENAME), 'File does not exist: %s' % FILENAME

## TEST: ATTEMPT TO PARSE STIG FILE
## REQUIRES: STIG (XML)
def test_convert_xccdf() -> None:
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
    STIG_JSON = stig_parser.convert_xccdf(RAW_FILE)

    ## ENSURE STIG WAS PARSED
    assert STIG_JSON is not None, 'Unable to Parse STIG File (%s)' % STIG_FILENAME

    ## VALIDATE KNOWN ENTRIES
    assert STIG_JSON['Title'] == "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide", "STIG Title Parsed Incorrectly"    ## STIG TITLE
    assert STIG_JSON['BenchmarkDate'] == "19 Jul 2019"     ## BENCHMARK DATE
    assert STIG_JSON['Rules'][0]['VulnID'] == "V-94863"     ## FIRST RULE ID
    assert STIG_JSON['ReleaseInfo'] == "Release: 1 Benchmark Date: 19 Jul 2019"    ## RELEASE INFO
    assert STIG_JSON['Source'] == "STIG.DOD.MIL"    ## SOURCE
    assert STIG_JSON['Notice'] == "terms-of-use"    ## NOTICE
    assert STIG_JSON['Rules'][0]['CCI'] == "CCI-000054"    ## FIRST RULE CCI NUMBER
    assert STIG_JSON['Rules'][0]['StigID'] == "DKER-EE-001000"     ## FIRST RULE STIG ID
    assert STIG_JSON['Rules'][0]['RuleID'] == "SV-104693r1_rule"   ## FIRST RULE ID

## TEST: ATTEMPT TO PARSE STIG FILE W/O EXTRACTING FILE
## REQUIRES: STIG (ZIP)
def test_convert_stig() -> None:
    ## CONVERT STIG TO JSON OBJECT
    STIG_JSON = stig_parser.convert_stig(FILENAME)

    ## ENSURE STIG WAS PARSED
    assert STIG_JSON is not None, 'Unable to Parse STIG File (%s)' % FILENAME

    ## VALIDATE KNOWN ENTRIES
    assert STIG_JSON['Title'] == "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide", "STIG Title Parsed Incorrectly"    ## STIG TITLE
    assert STIG_JSON['BenchmarkDate'] == "19 Jul 2019"     ## BENCHMARK DATE
    assert STIG_JSON['Rules'][0]['VulnID'] == "V-94863"     ## FIRST RULE ID
    assert STIG_JSON['ReleaseInfo'] == "Release: 1 Benchmark Date: 19 Jul 2019"    ## RELEASE INFO
    assert STIG_JSON['Source'] == "STIG.DOD.MIL"    ## SOURCE
    assert STIG_JSON['Notice'] == "terms-of-use"    ## NOTICE
    assert STIG_JSON['Rules'][0]['CCI'] == "CCI-000054"    ## FIRST RULE CCI NUMBER
    assert STIG_JSON['Rules'][0]['StigID'] == "DKER-EE-001000"     ## FIRST RULE STIG ID
    assert STIG_JSON['Rules'][0]['RuleID'] == "SV-104693r1_rule"   ## FIRST RULE ID

## TEST: EXTRACT STIG FROM ZIP
## REQUIRES: STIG (ZIP)
def test_extract_stig() -> None:
    ## CONVERT STIG TO JSON OBJECT
    STIG_JSON = stig_parser.convert_stig(FILENAME)

    ## ENSURE STIG WAS PARSED
    assert STIG_JSON is not None, 'Unable to Parse STIG File (%s)' % FILENAME

## TEST: ATTEMPT TO SAVE STIG TO JSON FILE
## REQUIRES: STIG (ZIP), EXPORT FILE PATH
def test_generate_stig_json() -> None:
    ## CONVERT STIG TO JSON OBJECT
    STIG_JSON = stig_parser.convert_stig(FILENAME)

    ## CREATE JSON FILE
    stig_parser.generate_stig_json(STIG_JSON, EXPORT_PATH_JSON)

    ## ENSURE FILE CREATION WAS SUCCESSFUL
    assert os.path.exists(EXPORT_PATH_JSON), "Exported File (%s) Doesn't Exist!" % EXPORT_PATH_JSON

    ## ATTEMPT TO READ JSON FILE TO ENSURE VALID EXPORT
    FILE = open(EXPORT_PATH_JSON, "r")
    STIG = json.load(FILE)

    ## ENSURE FIELDS ARE READABLE
    assert STIG['Title'] == "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide", "Unable to read JSON File (%s)" % EXPORT_PATH_JSON
    assert STIG['Rules'][0]['VulnID'] == "V-94863", "Unable to read JSON File (%s)" % EXPORT_PATH_JSON

    ## DELETE TEST FILES
    os.remove(EXPORT_PATH_JSON)

## TEST: ATTEMPT TO GENERATE A BLANK CHECKLIST (CKL) FILE
## REQUIRES: STIG (ZIP), CHECKLIST INFO (JSON)
def test_generate_ckl() -> None:
    ## ATTEMPT TO GENERATE CKL
    CKL = stig_parser.generate_ckl(FILENAME, CHECKLIST_INFO)

    ## VALIDATE RESPONSE RETURNED
    assert CKL is not None, 'Unable to generate CKL based upon the passed STIG File (%s)' % FILENAME

    ## CONVERT CHECKLIST (CKL) TO DICTIONARY
    CHECKLIST_DICT = convert_ckl_to_dict(CKL)

    ## VALIDATE CKL FIELDS (ASSET INFO)
    ASSET = CHECKLIST_DICT['CHECKLIST']['ASSET']
    assert ASSET['ROLE'] == "None", 'Checklist Asset Role is Incorrect. %s (From Function) =/= None' % ASSET['ROLE']        ## ASSET ROLE FIELD

    ## VALIDATE CKL FIELDS (STIG INFO)
    STIG = CHECKLIST_DICT['CHECKLIST']['STIGS']['iSTIG']['STIG_INFO']['SI_DATA']
    assert STIG[0]['SID_DATA'] == "1", 'STIG Version is Incorrect. %s (From Function) =/= 1' % STIG[0]['SID_DATA']                                                                      ## STIG VERSION FIELD
    assert STIG[3]['SID_DATA'] == "Docker_Enterprise_2-x_Linux-UNIX", 'STIG ID is Incorrect. %s (From Function) =/= Docker_Enterprise_2-x_Linux-UNIX_STIG' % STIG[3]['SID_DATA']   ## STIG ID

## TEST: GENERATE CKL FILE
## REQUIRES: CHECKLIST XML, OUTPUT FILENAME
def test_generate_ckl_file() -> None:
    ## ATTEMPT TO GENERATE CKL
    CKL = stig_parser.generate_ckl(FILENAME, CHECKLIST_INFO)

    ## VALIDATE RESPONSE RETURNED
    assert CKL is not None, 'Unable to generate CKL based upon the passed STIG File (%s)' % FILENAME

    ## OUTPUT CKL TO FILE
    stig_parser.generate_ckl_file(CKL, EXPORT_PATH_CKL)

    ## ENSURE FILE WAS CREATED
    assert os.path.exists(EXPORT_PATH_CKL), "Exported File (%s) Doesn't Exist!" % EXPORT_PATH_CKL

    ## ATTEMPT TO LOAD FILE TO ENSURE A VALID EXPORT
    FILE = open(EXPORT_PATH_CKL, "r")
    CHECKLIST = xmltodict.parse(FILE.read(), dict_constructor=dict)

    ## ENSURE FIELDS ARE READABLE
    assert CHECKLIST['CHECKLIST']['ASSET']['ROLE'] == "None", "Unable to read CKL File (%s)" % EXPORT_PATH_CKL

    ## DELETE TEST FILES
    os.remove(EXPORT_PATH_CKL)