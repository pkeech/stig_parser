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

        ## CONVERT IDENT ORDEREDDICT TO JSON
        IDENT = STIG['Rule']['ident']

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

        """
        [
            ('@system', 'http://iase.disa.mil/cci'), 
            ('#text', 'CCI-000054')
        ]
        """

      
        ## ADD TO ARRAY
        STIGS.append(oSTIG)

    ## ADD STIGS TO JSON OBJECT
    json_results['rules'] = STIGS

    ## RETURN RESULTS
    return json_results