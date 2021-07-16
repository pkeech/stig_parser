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
from xml.dom import minidom

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

    ## CREATE XML DOCUMENT
    DOC = minidom.Document()
    XML = DOC.createElement('CHECKLIST')

    ## ADD ROOT ELEMENT TO DOCUMENT
    DOC.appendChild(XML)

    ## ADD VERSION COMMENT LINE
    COMMENT = DOC.createComment('DISA STIG Viewer :: 2.14')
    DOC.appendChild(COMMENT)

    ## GENERATE ASSET INFORMATION
    ASSET_ELEMENT = helper.create_element(DOC, 'ASSET', '', XML)

    helper.create_element(DOC, "ROLE", CHECKLIST_INFO['ROLE'], ASSET_ELEMENT)                                  ## ASSET ROLE 
    helper.create_element(DOC, "ASSET_TYPE", CHECKLIST_INFO['ASSET_TYPE'], ASSET_ELEMENT)                      ## ASSET TYPE 
    helper.create_element(DOC, "HOST_NAME", CHECKLIST_INFO['HOST_NAME'], ASSET_ELEMENT)                        ## ASSET HOSTNAME 
    helper.create_element(DOC, "HOST_IP", CHECKLIST_INFO['HOST_IP'], ASSET_ELEMENT)                            ## ASSET IP 
    helper.create_element(DOC, "HOST_MAC", CHECKLIST_INFO['HOST_MAC'], ASSET_ELEMENT)                          ## ASSET MAC ADDRESS 
    helper.create_element(DOC, "HOST_FQDN", CHECKLIST_INFO['HOST_FQDN'], ASSET_ELEMENT)                        ## ASSET FQDN 
    helper.create_element(DOC, "TARGET_COMMENT", CHECKLIST_INFO['TARGET_COMMENT'], ASSET_ELEMENT)              ## ASSET TARGET COMMENT 
    helper.create_element(DOC, "TECH_AREA", CHECKLIST_INFO['TECH_AREA'], ASSET_ELEMENT)                        ## ASSET TECH AREA 
    helper.create_element(DOC, "TARGET_KEY", CHECKLIST_INFO['TARGET_KEY'], ASSET_ELEMENT)                      ## ASSET TARGET KEY 
    helper.create_element(DOC, "WEB_OR_DATABASE", CHECKLIST_INFO['WEB_OR_DATABASE'], ASSET_ELEMENT)            ## ASSET WEB OR DATABASE 
    helper.create_element(DOC, "WEB_DB_SITE", CHECKLIST_INFO['WEB_DB_SITE'], ASSET_ELEMENT)                    ## ASSET DB SITE 
    helper.create_element(DOC, "WEB_DB_INSTANCE", CHECKLIST_INFO['WEB_DB_INSTANCE'], ASSET_ELEMENT)            ## ASSET DB INSTANCE

    ## CREATE STIG STRUCTURE
    STIG_ELEMENT = helper.create_element(DOC, 'STIGS', '', XML)
    ISTIG_ELEMENT = helper.create_element(DOC, 'iSTIG', '', STIG_ELEMENT)
    STIGINFO_ELEMENT = helper.create_element(DOC, 'STIG_INFO', '', ISTIG_ELEMENT)

    ## GENERATE STIG_ID FIELD
    STIG_ID = JSON_STIG['Title'].replace(' Security Technical Implementation Guide', '').replace(' ', '_').replace('.', '-').replace('/', '-')

    ## CREATE STIG INFO ELEMENTS
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'version', 'SID_DATA', JSON_STIG['Version'], 'SI_DATA', STIGINFO_ELEMENT)                                             ## STIG VERSION
    
    ## TODO: DETERMINE CLASSIFICATION LEVEL
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'classification', 'SID_DATA', 'UNCLASSIFIED', 'SI_DATA', STIGINFO_ELEMENT)                           ## STIG CLASSIFICATION
    
    ## TODO: HANDLE CUSTOM NAME ATTRIBUTES
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'customname', 'SID_DATA', '', 'SI_DATA', STIGINFO_ELEMENT)                                           ## STIG CUSTOMNAME
    

    helper.create_two_elements_parent(DOC, 'SID_NAME', 'stigid', 'SID_DATA', STIG_ID, 'SI_DATA', STIGINFO_ELEMENT)          ## STIG ID
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'description', 'SID_DATA', JSON_STIG['Description'], 'SI_DATA', STIGINFO_ELEMENT)                                     ## STIG DESCRIPTION
    

    ## TODO: ADD STIG FILENAME TO JSON OBJECT
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'filename', 'SID_DATA', FILENAME, 'SI_DATA', STIGINFO_ELEMENT)                                       ## STIG FILENAME
    
    
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'releaseinfo', 'SID_DATA', JSON_STIG['ReleaseInfo'], 'SI_DATA', STIGINFO_ELEMENT)    ## STIG RELEASE INFO
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'title', 'SID_DATA', JSON_STIG['Title'], 'SI_DATA', STIGINFO_ELEMENT)                                             ## STIG TITLE
    

    ## TODO: DETERMINE UUID CREATION (IS IT RANDOMLY CREATED DURING CKL CREATION)
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'uuid', 'SID_DATA', 'eaab6cca-d77d-4787-868b-766afc44845d', 'SI_DATA', STIGINFO_ELEMENT)             ## STIG UUID
    
    
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'notice', 'SID_DATA', JSON_STIG['Notice'], 'SI_DATA', STIGINFO_ELEMENT)                                   ## STIG NOTICE
    helper.create_two_elements_parent(DOC, 'SID_NAME', 'source', 'SID_DATA', JSON_STIG['Source'], 'SI_DATA', STIGINFO_ELEMENT)                                               ## STIG SOURCE
    

    ## LOOP THROUGH VULNERABILITY RULE
    for RULE in JSON_STIG['Rules']:
        ## CREATE VULN ELEMENT
        VULN_ELEMENT = helper.create_element(DOC, 'VULN', '', ISTIG_ELEMENT)

        ## FORMAT OUTPUTS
        STIG_REF = JSON_STIG['Title'] + " :: " + JSON_STIG['Version']

        ## CREATE RULE ELEMENTS
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Vuln_Num', 'ATTRIBUTE_DATA', RULE['VulnID'], 'STIG_DATA', VULN_ELEMENT)                       ## VULNERABILITY NUMBER
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Severity', 'ATTRIBUTE_DATA', RULE['Severity'], 'STIG_DATA', VULN_ELEMENT)                     ## VULNERABILITY SEVERITY
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Group_Title', 'ATTRIBUTE_DATA', 'SRG-APP-000001', 'STIG_DATA', VULN_ELEMENT)                  ## VULNERABILITY GROUP TITLE
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Rule_ID', 'ATTRIBUTE_DATA', RULE['RuleID'], 'STIG_DATA', VULN_ELEMENT)                        ## VULNERABILITY RULE ID
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Rule_Ver', 'ATTRIBUTE_DATA', RULE['StigID'], 'STIG_DATA', VULN_ELEMENT)                       ## VULNERABILITY RULE VERSION
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Rule_Title', 'ATTRIBUTE_DATA', RULE['RuleTitle'], 'STIG_DATA', VULN_ELEMENT)                  ## VULNERABILITY RULE TITLE
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Vuln_Discuss', 'ATTRIBUTE_DATA', RULE['VulnDiscussion'], 'STIG_DATA', VULN_ELEMENT)           ## VULNERABILITY DISCUSSION
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'IA_Controls', 'ATTRIBUTE_DATA', RULE['IAControls'], 'STIG_DATA', VULN_ELEMENT)                ## VULNERABILITY IA CONTROL
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Check_Content', 'ATTRIBUTE_DATA', RULE['CheckText'], 'STIG_DATA', VULN_ELEMENT)               ## VULNERABILITY CHECK CONTENT
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Fix_Text', 'ATTRIBUTE_DATA', RULE['FixText'], 'STIG_DATA', VULN_ELEMENT)                      ## VULNERABILITY FIX TEXT
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'False_Positives', 'ATTRIBUTE_DATA', RULE['FalsePositives'], 'STIG_DATA', VULN_ELEMENT)        ## VULNERABILITY FALSE POSITIVIES        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'False_Negatives', 'ATTRIBUTE_DATA', RULE['FalseNegatives'], 'STIG_DATA', VULN_ELEMENT)        ## VULNERABILITY FALSE NEGATIVES
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Documentable', 'ATTRIBUTE_DATA', RULE['Documentable'], 'STIG_DATA', VULN_ELEMENT)             ## VULNERABILITY DOCUMENTABLE        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Mitigations', 'ATTRIBUTE_DATA', RULE['Mitigations'], 'STIG_DATA', VULN_ELEMENT)               ## VULNERABILITY MITIGATION        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Potential_Impact', 'ATTRIBUTE_DATA', RULE['PotentialImpacts'], 'STIG_DATA', VULN_ELEMENT)     ## VULNERABILITY POTENTIAL IMPACT        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Third_Party_Tools', 'ATTRIBUTE_DATA', RULE['ThirdPartyTools'], 'STIG_DATA', VULN_ELEMENT)     ## VULNERABILITY THIRD PARTY TOOLS
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Mitigation_Control', 'ATTRIBUTE_DATA', RULE['MitigationControl'], 'STIG_DATA', VULN_ELEMENT)  ## VULNERABILITY MITIGATION CONTROLS
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Responsibility', 'ATTRIBUTE_DATA', RULE['Responsibility'], 'STIG_DATA', VULN_ELEMENT)         ## VULNERABILITY RESPONSIBILITY        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Security_Override_Guidance', 'ATTRIBUTE_DATA', RULE['SeverityOverrideGuidance'], 'STIG_DATA', VULN_ELEMENT)     ## VULNERABILITY SECURITY OVERRIDE GUIDE
        ## TODO: PARSE 'description' field for <IAControls>
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Check_Content_Ref', 'ATTRIBUTE_DATA', 'M', 'STIG_DATA', VULN_ELEMENT)             ## VULNERABILITY CHECK CONTENT REFERENCE
        
        ## TODO: DETERMINE STIG RULE WEIGHT
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Weight', 'ATTRIBUTE_DATA', '10.0', 'STIG_DATA', VULN_ELEMENT)                     ## VULNERABILITY WEIGHT
        
        ## TODO: DETERMINE STIG CLASSIFICATION
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'Class', 'ATTRIBUTE_DATA', 'Unclass', 'STIG_DATA', VULN_ELEMENT)                   ## VULNERABILITY CLASSIFICATION
        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'STIGRef', 'ATTRIBUTE_DATA', STIG_REF, 'STIG_DATA', VULN_ELEMENT)                      ## VULNERABILITY STIG REFERENCE
        
        ## TODO: FIND TARGET KEY
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'TargetKey', 'ATTRIBUTE_DATA', '3425', 'STIG_DATA', VULN_ELEMENT)                  ## VULNERABILITY TARGET KEY
        
        ## TODO: FIND RULE UUID
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'STIG_UUID', 'ATTRIBUTE_DATA', '000000000000000000000000000', 'STIG_DATA', VULN_ELEMENT)               ## VULNERABILITY UUID
        
        ## TODO: DETERMINE LEGACY_ID ATTRIBUTE
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'LEGACY_ID', 'ATTRIBUTE_DATA', '', 'STIG_DATA', VULN_ELEMENT)                      ## VULNERABILITY LEGACY ID
        
        
        helper.create_two_elements_parent(DOC, 'VULN_ATTRIBUTE', 'CCI_REF', 'ATTRIBUTE_DATA', RULE['CCI'], 'STIG_DATA', VULN_ELEMENT)              ## VULNERABILITY CCI REFERENCE


    ## RULE STATUS ELEMENTS
    helper.create_element(DOC, 'STATUS', "Not_Reviewed", VULN_ELEMENT)          ## VULNERABILITY FINDING STATUS
    helper.create_element(DOC, 'FINDING_DETAILS', "", VULN_ELEMENT)             ## VULNERABILITY FINDING DETAILS
    helper.create_element(DOC, 'COMMENTS', "", VULN_ELEMENT)                    ## VULNERABILITY COMMENTS
    helper.create_element(DOC, 'SEVERITY_OVERRIDE', "", VULN_ELEMENT)           ## VULNERABILITY SEVERITY OVERRIDE
    helper.create_element(DOC, 'SEVERITY_JUSTIFICATION', "", VULN_ELEMENT)      ## VULNERABILITY SEVERITY JUSTIFICATION

    ## FORMAT XML OBJECT & ENCODE
    FORMAT_XML = DOC.toprettyxml(indent ="\t", encoding="utf-8")

    ## RETURN CHECKLIST
    return FORMAT_XML

## FUNCTION: GENERATE CHECKLIST FILE (CKL)
def generate_ckl_file(CKL, FILENAME):
    ## SAVE XML OBJECT TO FILE
    with open(FILENAME, "wb") as FILE:
        FILE.write(CKL)