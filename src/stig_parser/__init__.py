##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : 1.0.2
##  Description : STIG-Parser v1.0.2 Module
##  Requirements: xmltodict
##  Build       : docker run -it --rm -v $(PWD):/stig-parser python /bin/bash
##                cd stig-parser
##                python3 -m pip install --upgrade build
##                python3 -m build
##                

## IMPORT REQUIRED EXTERNAL MODULES
import os, xmltodict, json

## FUNCTION: CONVERT RAW XCCDF (XML) TO JSON
def convert_xccdf(raw):
    
    ## CONVERT XML TO PYTHON DICTIONARY
    content_dict = xmltodict.parse(raw, dict_constructor=dict)

    ## HANDLE NEW VS. OLD VERSION OF STIG SCHEMA (ISSUE #3)
    if isinstance(content_dict['Benchmark']['plain-text'], list):
        ## NEW VERSION
        raw_version = content_dict['Benchmark']['plain-text'][0]['#text']
    else:
        ## OLD VERSION
        raw_version = content_dict['Benchmark']['plain-text']['#text']        

    ## SAVE RELEASE INFO
    release_info = raw_version

    ## FORMAT RELEASE INFO FOR SPECIFIC DATA FIELDS
    raw_version = raw_version.split('Benchmark Date: ')
    BENCH_DATE = raw_version[1]
    REL = raw_version[0].replace('Release: ','')

    ## CREATE RETURNED JSON STRUCTURE
    json_results = {
        "title": content_dict['Benchmark']['title'],
        "description": content_dict['Benchmark']['description'],
        "version": content_dict['Benchmark']['version'],
        "release": REL,
        "benchmark_date": BENCH_DATE,
        "release_info": release_info,
        "source": content_dict['Benchmark']['reference']['dc:source'],
        "notice": content_dict['Benchmark']['notice']['@id']
    }

    ## GENERATE EMPTY ARRAY
    STIGS = []

    ## LOOP THROUGH STIGS
    for STIG in content_dict['Benchmark']['Group']:

        ## PARSE IDENT 
        IDENT = STIG['Rule']['ident']

        ## HANDLE MULTIPLE IDENT ENTRIES
        if len(IDENT) == 2:
            IDENT = IDENT['#text']
        else:
            ## DEFINE EMPTY RESULTS
            RESULTS = ""
        
            ## LOOP THROUGH ALL CCI NUMBERS
            for result in IDENT:
                RESULTS += result['#text'] + ","

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
    json_results['rules'] = STIGS

    ## RETURN RESULTS
    return json_results