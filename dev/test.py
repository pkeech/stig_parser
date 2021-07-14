##  ===================================
##  ===== STIG PARSER TEST SCRIPT =====
##  ===================================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : TEST
##  Description : Test Creation of Blank CKL File
##  Requirements: STIG File (ZIP), stig_parser (pip)
##  Development : docker run -it --rm -v $(PWD)/dev:/testing python /bin/bash

## IMPORT REQUIREMENTS
import zipfile, json
from stig_parser import convert_xccdf
#from checklist import create_checklist

## DEBUG: STATIC VARIABLES FOR TESTING PURPOSES
COMPRESSED_ZIP = "U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip"
RAW_NAME = COMPRESSED_ZIP.replace(".zip", "")

## DETERMINE STIG VERSION
RAW_NAME = RAW_NAME.split("_")
STIG_VERSION = RAW_NAME[-2]

## DETERMINE STIG NAME
RAW_NAME = COMPRESSED_ZIP.replace(".zip", "")
STIG_NAME = RAW_NAME.replace(("_" + STIG_VERSION + "_STIG"), "")

## OPEN XML FILE FROM ZIP FILE AND OBTAIN LIST OF FILES
z = zipfile.ZipFile(COMPRESSED_ZIP)
files = z.namelist()

## FIND MANUAL STIG FILE
for file in files:
    if file.endswith('_Manual-xccdf.xml'):
        ## HANDLE MACOS
        if not file.startswith('__MACOS'):
            ## DETERMINE FILE NAME
            print ("[INFO] STIG Filename: " + file)
            FILENAME = file
            break

## READ STIG FILE
rawFile = z.read(FILENAME)

## CONVERT RAW STIG TO JSON OBJECT
STIG_JSON = convert_xccdf(rawFile)

## GENERATE BLANK CHECKLIST
#Checklist = create_checklist(STIG_JSON, FILENAME)

## DEBUG
#print(Checklist.toJSON())

## DEBUG: Pretty Print STIG JSON Object
#print(json.dumps(STIG_JSON, indent=4))

## DEBUG: Write JSON to File
with open('dump.json', 'w') as outfile:
    json.dump(STIG_JSON, outfile, indent=4)