##########################
##  STIG PARSER MODULE  ##
##########################

## IMPORT REQUIRED EXTERNAL MODULES
import os, xmltodict, json
#from pkg_resources import resource_filename


## FUNCTION: CONVERT RAW XCCDF (XML) TO JSON
def convert_xccdf(raw):
    ## CREATE XSD PATH
    #filepath = resource_filename(__name__, 'xccdf-1.1.4.xsd')
        
    ## CONVERT XML TO PYTHON DICTIONARY
    content_dict = xmltodict.parse(raw)

    ## HANDLE NEW VS. OLD VERSION OF STIG SCHEMA (ISSUE #3)
    if isinstance(content_dict['Benchmark']['plain-text'], list):
        ## NEW VERSION
        raw_version = content_dict['Benchmark']['plain-text'][0]['#text']
    else:
        ## OLD VERSION
        raw_version = content_dict['Benchmark']['plain-text']['#text']        

    ## PARSE DATE AND RELEASE DATA
    raw_version = raw_version.split('Benchmark Date: ')
    BENCH_DATE = raw_version[1]
    REL = raw_version[0].replace('Release: ','')

    ## CREATE RETURNED JSON STRUCTURE
    json_results = {
        "title": content_dict['Benchmark']['title'],
        "description": content_dict['Benchmark']['description'],
        "version": content_dict['Benchmark']['version'],
        "release": REL,
        "benchmark_date": BENCH_DATE
    }

    ## GENERATE EMPTY ARRAY
    STIGS = []

    ## LOOP THROUGH STIGS
    for STIG in content_dict['Benchmark']['Group']:

        ## DEFINE STIG
        oSTIG = {
            'id': STIG['@id'],
            'stig_id': STIG['title'],
            'severity': STIG['Rule']['@severity'],
            'title': STIG['Rule']['title'],
            'description': STIG['Rule']['description'],
            'fixtext': STIG['Rule']['fixtext']['#text'],
            'check': STIG['Rule']['check']['check-content']
        }
      
        ## ADD TO ARRAY
        STIGS.append(oSTIG)

    ## ADD STIGS TO JSON OBJECT
    json_results['rules'] = STIGS

    ## RETURN RESULTS
    return json_results
