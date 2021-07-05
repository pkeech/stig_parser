##  ===================================
##  ===== STIG PARSER TEST SCRIPT =====
##  ===================================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : TEST
##  Description : Test Creation of Blank CKL File
##  Requirements: STIG File (ZIP), 

## docker run -it --rm -v $(PWD)/dev:/testing python /bin/bash

## IMPORT REQUIREMENTS
import zipfile

## DEBUG: STATIC VARIABLES FOR TESTING PURPOSES
COMPRESSED_ZIP = "U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG.zip"
RAW_NAME = COMPRESSED_ZIP.replace(".zip", "")

## DETERMINE STIG VERSION
RAW_NAME = RAW_NAME.split("_")
STIG_VERSION = RAW_NAME[-2]

## DETERMINE STIG NAME
RAW_NAME = COMPRESSED_ZIP.replace(".zip", "")
STIG_NAME = RAW_NAME.replace(("_" + STIG_VERSION + "_STIG"), "")

## DETERMINE FILE NAME



print("Version: " + STIG_VERSION)
print("Name: " + STIG_NAME)

STIG_NAME = COMPRESSED_ZIP.split(".")
STIG_PATH = STIG_NAME[0].replace("_STIG", "")
STIG_PATH = STIG_PATH + "_Manual_STIG"
STIG_PATH = STIG_NAME[0] + "/" + STIG_PATH + "/" + (STIG_PATH.replace("_STIG", "")) + "-xccdf.xml"


## DEBUG
#print ("[INFO] Source STIG ZIP File:     " + COMPRESSED_ZIP)
#print ("[INFO] STIG Name:                " + STIG_NAME[0])
#print ("[INFO] Path to XML File:         " + STIG_PATH)


#  U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml
#                                                                                                   U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG
#  U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG-xccdf.xml
#  U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual_STIG/U_Docker_Enterprise_2-x_Linux-UNIX_V1R1_Manual-xccdf.xml


## OPEN XML FILE FROM ZIP FILE
z = zipfile.ZipFile(COMPRESSED_ZIP)


#files = z.namelist()

#for file in files:
#    if file == STIG_PATH:
#        print ("-----> " + file)
#    else:
#        print (file)

#f = z.open(STIG_PATH)

#with zipfile.ZipFile('/path/to/my_file.apk') as z:
#    with open('temp/icon.png', 'wb') as f:
#        f.read(z.read('/res/drawable/icon.png'))