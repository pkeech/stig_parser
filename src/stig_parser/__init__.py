##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : 1.1.0
##  Description : STIG-Parser 1.1.0 Module
##  Requirements: xmltodict              

## IMPORT REQUIRED EXTERNAL MODULES
import os, xmltodict, zipfile, json, uuid
#from xml.dom import minidom
import xml.etree.cElementTree as ET

## IMPORT HELPER FUNCTIONS
import src.stig_parser.helpers as helper

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

    ## CREATE RETURNED STIG JSON
    ## TODO: ADD STIG FILENAME
    JSON_RESULTS = {
        "Title": CONTENT_DICT['Benchmark']['title'],
        "Description": CONTENT_DICT['Benchmark']['description'],
        "Version": CONTENT_DICT['Benchmark']['version'],
        "Release": REL,
        "BenchmarkDate": BENCH_DATE,
        "ReleaseInfo": RELEASE_INFO,
        "Source": CONTENT_DICT['Benchmark']['reference']['dc:source'],
        "Notice": CONTENT_DICT['Benchmark']['notice']['@id']
    }

    ## GENERATE EMPTY ARRAY
    STIGS = []

    ## LOOP THROUGH STIGS
    for STIG in CONTENT_DICT['Benchmark']['Group']:

        ## PARSE IDENT 
        IDENT = STIG['Rule']['ident']

        ## HANDLE MULTIPLE IDENT ENTRIES (CCI)
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
        
        ## FORMAT SEVERITY
        ## TODO: DOCUMENT WHY THIS IS HAPPENING. STIGVIEWER CONVERTS LOW/MED/HIGH TO CAT III/CAT II/CAT I
        if STIG['Rule']['@severity'] == "high":
            CAT = "CAT I"
        elif STIG['Rule']['@severity'] == "medium":
            CAT = "CAT II"
        elif STIG['Rule']['@severity'] == "low":
            CAT = "CAT III"
        else:
            CAT = ""

        ## DEFINE RULE STRUCTURE
        oSTIG = {
            'VulnID': STIG['@id'],
            'RuleID': STIG['Rule']['@id'],
            'StigID': STIG['Rule']['version'],
            'Severity': STIG['Rule']['@severity'],
            'Cat': CAT,
            ## TODO: DETERMINE STIG RULE CLASSIFICATION
            'Classification': "",
            'GroupTitle': STIG['title'],
            'RuleTitle': STIG['Rule']['title'],
            'Description': STIG['Rule']['description'],
            'VulnDiscussion': helper.find_between(STIG['Rule']['description'], "<VulnDiscussion>", "</VulnDiscussion>"),
            'FalsePositives': helper.find_between(STIG['Rule']['description'], "<FalsePositives>", "</FalsePositives>"),
            'FalseNegatives': helper.find_between(STIG['Rule']['description'], "<FalseNegatives>", "</FalseNegatives>"),
            'Documentable': helper.find_between(STIG['Rule']['description'], "<Documentable>", "</Documentable>"),
            'Mitigations': helper.find_between(STIG['Rule']['description'], "<Mitigations>", "</Mitigations>"),
            'SeverityOverrideGuidance': helper.find_between(STIG['Rule']['description'], "<SeverityOverrideGuidance>", "</SeverityOverrideGuidance>"),
            'PotentialImpacts': helper.find_between(STIG['Rule']['description'], "<PotentialImpacts>", "</PotentialImpacts>"),
            'ThirdPartyTools': helper.find_between(STIG['Rule']['description'], "<ThirdPartyTools>", "</ThirdPartyTools>"),
            'MitigationControl': helper.find_between(STIG['Rule']['description'], "<MitigationControl>", "</MitigationControl>"),
            'Responsibility': helper.find_between(STIG['Rule']['description'], "<Responsibility>", "</Responsibility>"),
            'IAControls': helper.find_between(STIG['Rule']['description'], "<IAControls>", "</IAControls>"),
            'CheckText': STIG['Rule']['check']['check-content'],
            'FixText': STIG['Rule']['fixtext']['#text'],
            'CCI': IDENT,
        }

        ## ADD TO ARRAY
        STIGS.append(oSTIG)

    ## ADD STIGS TO JSON OBJECT
    JSON_RESULTS['Rules'] = STIGS

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

## FUNCTION: CREATE STIG JSON FILE
def generate_stig_json(JSON_STIG, EXPORT_FILE):
    ## CREATE JSON FILE AND SAVE
    with open(EXPORT_FILE, 'w') as FILE:
        json.dump(JSON_STIG, FILE, indent=4)

## FUNCTION: GENERATE BLANK CHECKLIST
def generate_ckl(FILENAME, CHECKLIST_INFO):
    ## EXTRACT STIG FROM ZIP FILE
    RAW_STIG = extract_stig(FILENAME)
    
    ## CONVERT TO JSON
    JSON_STIG = convert_xccdf(RAW_STIG)

    ## GENERATE STIG_UUID
    STIG_UUID = uuid.uuid4()

    ## GENERATE XML STRUCTURE
    ROOT = ET.Element('CHECKLIST')

    ## ADD STIG VIEWER COMMENT
    COMMENT = ET.Comment('DISA STIG Viewer :: 2.14')
    ROOT.append(COMMENT)

    ## ADD ASSET ELEMENT
    ASSET = ET.SubElement(ROOT, 'ASSET')

    ## GENERATE ASSET ELEMENTS
    ET.SubElement(ASSET, 'ROLE').text = CHECKLIST_INFO.get('ROLE')                          ## ASSET ROLE
    ET.SubElement(ASSET, 'ASSET_TYPE').text = CHECKLIST_INFO.get('ASSET_TYPE')              ## ASSET TYPE 
    ET.SubElement(ASSET, 'HOST_NAME').text = CHECKLIST_INFO.get('HOST_NAME')                ## ASSET HOSTNAME
    ET.SubElement(ASSET, 'HOST_IP').text = CHECKLIST_INFO.get('HOST_IP')                    ## ASSET IP
    ET.SubElement(ASSET, 'HOST_MAC').text = CHECKLIST_INFO.get('HOST_MAC')                  ## ASSET MAC ADDRESS 
    ET.SubElement(ASSET, 'HOST_FQDN').text = CHECKLIST_INFO.get('HOST_FQDN')                ## ASSET FQDN
    ET.SubElement(ASSET, 'TARGET_COMMENT').text = CHECKLIST_INFO.get('TARGET_COMMENT')      ## ASSET TARGET COMMENT
    ET.SubElement(ASSET, 'TECH_AREA').text = CHECKLIST_INFO.get('TECH_AREA')                ## ASSET TECH AREA 
    ET.SubElement(ASSET, 'TARGET_KEY').text = CHECKLIST_INFO.get('TARGET_KEY')              ## ASSET TARGET KEY
    ET.SubElement(ASSET, 'WEB_OR_DATABASE').text = CHECKLIST_INFO.get('WEB_OR_DATABASE')    ## ASSET WEB OR DATABASE
    ET.SubElement(ASSET, 'WEB_DB_SITE').text = CHECKLIST_INFO.get('WEB_DB_SITE')            ## ASSET DB SITE 
    ET.SubElement(ASSET, 'WEB_DB_INSTANCE').text = CHECKLIST_INFO.get('WEB_DB_INSTANCE')    ## ASSET DB INSTANCE

    ## GENERATE STIG, ISTIG, STIG_INFO AND VULN ELEMENTS
    STIGS = ET.SubElement(ROOT, 'STIGS')
    ISTIG = ET.SubElement(STIGS, 'iSTIG')
    STIG_INFO = ET.SubElement(ISTIG, 'STIG_INFO')

    ## FORMAT STIG_ID FIELD
    STIG_ID = JSON_STIG['Title'].replace(' Security Technical Implementation Guide', '').replace(' ', '_').replace('.', '-').replace('/', '-')

    ## GENERATE STIG_INFO FIELDS
    ## TODO: CLASSIFICATION, CUSTOM NAME, FILENAME
    helper.generate_stig_info(STIG_INFO, 'version', JSON_STIG['Version'])                   ## STIG VERSION
    helper.generate_stig_info(STIG_INFO, 'classification', 'UNCLASSIFIED')          ## STIG CLASSIFICATION
    helper.generate_stig_info(STIG_INFO, 'customname', None)                        ## STIG CUSTOM NAME
    helper.generate_stig_info(STIG_INFO, 'stigid', STIG_ID)                                 ## STIG ID
    helper.generate_stig_info(STIG_INFO, 'description', JSON_STIG['Description'])           ## STIG DESCRIPTION
    helper.generate_stig_info(STIG_INFO, 'filename', 'TEMP FILENAME')               ## STIG FILENAME
    helper.generate_stig_info(STIG_INFO, 'releaseinfo', JSON_STIG['ReleaseInfo'])           ## STIG RELEASE INFO
    helper.generate_stig_info(STIG_INFO, 'title', JSON_STIG['Title'])                       ## STIG TITLE
    helper.generate_stig_info(STIG_INFO, 'uuid', str(uuid.uuid4()))                         ## STIG UUID
    helper.generate_stig_info(STIG_INFO, 'notice', JSON_STIG['Notice'])                     ## STIG NOTICE
    helper.generate_stig_info(STIG_INFO, 'source', JSON_STIG['Source'])                     ## STIG SOURCE

    ## GENERATE VULNERABILITIES
    for RULE in JSON_STIG['Rules']:
        
        ## CREATE VULN ELEMENT
        VULN = ET.SubElement(ISTIG, 'VULN')

        ## FORMAT RULE OUTPUTS
        STIG_REF = JSON_STIG['Title'] + " :: " + JSON_STIG['Version']

        ## CREATE RULES
        ## TODO: Group_Title, Check_Content_Ref, Weight, Classification, TargetKey, Legacy_ID
        helper.generate_vuln(VULN, 'Vuln_Num', RULE['VulnID'])                                         ## VULN ID
        helper.generate_vuln(VULN, 'Severity', RULE['Severity'])                                       ## VULN SEVERITY
        helper.generate_vuln(VULN, 'Group_Title', 'SRG-APP-000001')                            ## VULNERABILITY GROUP TITLE
        helper.generate_vuln(VULN, 'Rule_ID', RULE['RuleID'])                                          ## VULNERABILITY RULE ID
        helper.generate_vuln(VULN, 'Rule_Ver', RULE['StigID'])                                         ## VULNERABILITY RULE VERSION
        helper.generate_vuln(VULN, 'Rule_Title', RULE['RuleTitle'])                                    ## VULNERABILITY RULE TITLE
        helper.generate_vuln(VULN, 'Vuln_Discuss', RULE['VulnDiscussion'])                             ## VULNERABILITY DISCUSSION
        helper.generate_vuln(VULN, 'IA_Controls', RULE['IAControls'])                                  ## VULNERABILITY IA CONTROL
        helper.generate_vuln(VULN, 'Check_Content', RULE['CheckText'])                                 ## VULNERABILITY CHECK CONTENT
        helper.generate_vuln(VULN, 'Fix_Text', RULE['FixText'])                                        ## VULNERABILITY FIX TEXT
        helper.generate_vuln(VULN, 'False_Positives', RULE['FalsePositives'])                          ## VULNERABILITY FALSE POSITIVIES        
        helper.generate_vuln(VULN, 'False_Negatives', RULE['FalseNegatives'])                          ## VULNERABILITY FALSE NEGATIVES
        helper.generate_vuln(VULN, 'Documentable', RULE['Documentable'])                               ## VULNERABILITY DOCUMENTABLE        
        helper.generate_vuln(VULN, 'Mitigations', RULE['Mitigations'])                                 ## VULNERABILITY MITIGATION        
        helper.generate_vuln(VULN, 'Potential_Impact', RULE['PotentialImpacts'])                       ## VULNERABILITY POTENTIAL IMPACT        
        helper.generate_vuln(VULN, 'Third_Party_Tools', RULE['ThirdPartyTools'])                       ## VULNERABILITY THIRD PARTY TOOLS
        helper.generate_vuln(VULN, 'Mitigation_Control', RULE['MitigationControl'])                    ## VULNERABILITY MITIGATION CONTROLS
        helper.generate_vuln(VULN, 'Responsibility', RULE['Responsibility'])                           ## VULNERABILITY RESPONSIBILITY        
        helper.generate_vuln(VULN, 'Security_Override_Guidance', RULE['SeverityOverrideGuidance'])     ## VULNERABILITY SECURITY OVERRIDE GUIDE
        helper.generate_vuln(VULN, 'Check_Content_Ref', 'M')                                 ## VULNERABILITY CHECK CONTENT REFERENCE
        helper.generate_vuln(VULN, 'Weight', '10.0')                                         ## VULNERABILITY WEIGHT
        helper.generate_vuln(VULN, 'Class', 'Unclass')                                       ## VULNERABILITY CLASSIFICATION
        helper.generate_vuln(VULN, 'STIGRef', STIG_REF)                                                ## VULNERABILITY STIG REFERENCE
        helper.generate_vuln(VULN, 'TargetKey', '3425')                                      ## VULNERABILITY TARGET KEY
        helper.generate_vuln(VULN, 'STIG_UUID', str(STIG_UUID))                                        ## VULNERABILITY UUID
        helper.generate_vuln(VULN, 'LEGACY_ID', '')                                          ## VULNERABILITY LEGACY ID
        helper.generate_vuln(VULN, 'CCI_REF', RULE['CCI'])                                             ## VULNERABILITY CCI REFERENCE

        ## RULE STATUS ELEMENTS
        ET.SubElement(VULN, "STATUS").text = "Not_Reviewed"         ## VULNERABILITY FINDING STATUS
        ET.SubElement(VULN, 'FINDING_DETAILS').text = ""            ## VULNERABILITY FINDING DETAILS
        ET.SubElement(VULN, 'COMMENTS').text = ""                   ## VULNERABILITY COMMENTS
        ET.SubElement(VULN, 'SEVERITY_OVERRIDE').text = ""          ## VULNERABILITY SEVERITY OVERRIDE
        ET.SubElement(VULN, 'SEVERITY_JUSTIFICATION').text = ""     ## VULNERABILITY SEVERITY JUSTIFICATION

    ## FORMAT EXPORT    
    OUTPUT = ET.tostring(ROOT, encoding='UTF-8', xml_declaration=True, short_empty_elements=False)

    ## RETURN CHECKLIST
    return OUTPUT

## FUNCTION: GENERATE CHECKLIST FILE (CKL)
def generate_ckl_file(CKL, FILENAME):
    ## SAVE XML OBJECT TO FILE
    with open(FILENAME, "wb") as FILE:
        FILE.write(CKL)