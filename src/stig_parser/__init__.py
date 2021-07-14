##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : 1.1.0
##  Description : STIG-Parser 1.1.0 Module
##  Requirements: xmltodict              

## IMPORT REQUIRED EXTERNAL MODULES
import os, xmltodict, zipfile, json

## IMPORT HELPER FUNCTIONS
import helpers as helper

##  ---------------------
##  ----- FUNCTIONS -----
##  ---------------------

## FUNCTION: CONVERT RAW XCCDF (XML) TO JSON
def convert_xccdf(RAW):
    
    ## CONVERT XML TO PYTHON DICTIONARY
    CONTENT_DICT = xmltodict.parse(RAW, dict_constructor=dict)

    ## HANDLE NEW VS. OLD VERSION OF STIG SCHEMA (ISSUE #3)
    if isinstance(CONTENT_DICT['Benchmark']['plain-text'], list):
        ## NEW VERSION
        RAW_VERSION = CONTENT_DICT['Benchmark']['plain-text'][0]['#text']
    else:
        ## OLD VERSION
        RAW_VERSION = CONTENT_DICT['Benchmark']['plain-text']['#text']        

    ## SAVE RELEASE INFO
    RELEASE_INFO = RAW_VERSION

    ## FORMAT RELEASE INFO FOR SPECIFIC DATA FIELDS
    RAW_VERSION = RAW_VERSION.split('Benchmark Date: ')
    BENCH_DATE = RAW_VERSION[1]
    REL = RAW_VERSION[0].replace('Release: ','')

    ## CREATE RETURNED JSON STRUCTURE
    JSON_RESULTS = {
        "title": CONTENT_DICT['Benchmark']['title'],
        "description": CONTENT_DICT['Benchmark']['description'],
        "version": CONTENT_DICT['Benchmark']['version'],
        "release": REL,
        "benchmark_date": BENCH_DATE,
        "release_info": RELEASE_INFO,
        "source": CONTENT_DICT['Benchmark']['reference']['dc:source'],
        "notice": CONTENT_DICT['Benchmark']['notice']['@id']
    }

    ## GENERATE EMPTY ARRAY
    STIGS = []

    ## LOOP THROUGH STIGS
    for STIG in CONTENT_DICT['Benchmark']['Group']:

        ## PARSE IDENT 
        IDENT = STIG['Rule']['ident']

        ## HANDLE MULTIPLE IDENT ENTRIES
        if len(IDENT) == 2:
            IDENT = IDENT['#text']
        else:
            ## DEFINE EMPTY RESULTS
            RESULTS = ""
        
            ## LOOP THROUGH ALL CCI NUMBERS
            for RESULT in IDENT:
                RESULTS += RESULT['#text'] + ","

            ## REMOVE LAST ','
            IDENT = RESULTS.rstrip(RESULTS[-1])
         
        ## DEFINE STIG
        oSTIG = {
            'id': STIG['@id'],
            'stig_id': STIG['title'],
            'severity': STIG['Rule']['@severity'],
            'title': STIG['Rule']['title'],
            'description': STIG['Rule']['description'],
            'fixtext': STIG['Rule']['fixtext']['#text'],
            'check': STIG['Rule']['check']['check-content'],
            'cci': IDENT,
            'stig_id': STIG['Rule']['version'],
            'rule_id': STIG['Rule']['@id']
        }
              
        ## ADD TO ARRAY
        STIGS.append(oSTIG)

    ## ADD STIGS TO JSON OBJECT
    JSON_RESULTS['rules'] = STIGS

    ## RETURN RESULTS
    return JSON_RESULTS

## FUNCTION: EXTRACT STIG FROM ZIP FILE
def extract_stig(FILENAME):
    ## OPEN XML FILE FROM ZIP FILE AND OBTAIN LIST OF FILES
    ZIP = zipfile.ZipFile(FILENAME)
    FILES = ZIP.namelist()

    ## FIND MANUAL STIG FILE
    for FILE in FILES:
        if FILE.endswith('_Manual-xccdf.xml'):
            ## HANDLE MACOS
            if not FILE.startswith('__MACOS'):
                ## DETERMINE FILE NAME
                STIG_FILENAME = FILE
                break

    ## ENSURE FILE IS FOUND
    assert STIG_FILENAME is not None, 'Manual STIG File was NOT FOUND'

    ## READ STIG FILE
    RAW_FILE = ZIP.read(STIG_FILENAME) 

    ## RETURN RAW STIG
    return RAW_FILE

## FUNCTION: CONVERT STIG (ZIP) TO JSON FILE
def convert_stig(FILENAME):
    ## EXTRACT STIG FROM ZIP FILE
    RAW_STIG = extract_stig(FILENAME)
    
    ## CONVERT TO JSON
    RESULTS = convert_xccdf(RAW_STIG)

    ## RETURN JSON STIG
    return RESULTS

## FUNCTION: GENERATE BLANK CHECKLIST (CKL)
def generate_ckl(FILENAME, CHECKLIST_INFO):
    ## EXTRACT STIG FROM ZIP FILE
    RAW_STIG = extract_stig(FILENAME)
    
    ## CONVERT TO JSON
    JSON_STIG = convert_xccdf(RAW_STIG)

    ## CREATE XML DOCUMENT

    ## LINE 57 -------------------->
    ## LINE 57 -------------------->
    ## LINE 57 -------------------->
    ## LINE 57 -------------------->




    ## RETURN CHECKLIST
    return None