##########################
##  STIG PARSER MODULE  ##
##########################

## IMPORT REQUIRED EXTERNAL MODULES
import os, xmltodict, json
#from pkg_resources import resource_filename


## FUNCTION: CONVERT RAW XCCDF (XML) TO JSON
def convert_xccdf(raw):
    
    ## ----------------
    ## ----- TEST -----
    ## ----------------
    # docker run -it python /bin/bash
    # pip install stig-parser
    # mkdir docker && cd docker
    # curl https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip --output docker_stig.zip
    # unzip docker_stig.zip
    # python
    # 
    # from stig_parser import convert_xccdf
    # import json
    # f = open('/docker/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml', 'r')
    # temp = convert_xccdf(f.read())
    # print(json.dumps(temp, indent=4, sort_keys=True))
    #
    # f = open('/docker/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml', 'r')
    # content_dict = xmltodict.parse(f.read())
    # print(json.dumps(content_dict, indent=4, sort_keys=True))
    #
    #
    # output = open('/docker/output.txt', 'w')
    # print(json.dumps(content_dict, indent=4, sort_keys=True), file = output)
    # output.close()



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

            ## Rule ID
            ## STIG ID
            ## Classification
            ## CCI #
        }
      
        ## ADD TO ARRAY
        STIGS.append(oSTIG)

    ## ADD STIGS TO JSON OBJECT
    json_results['rules'] = STIGS

    ## RETURN RESULTS
    return json_results
