##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Description : Helper File
##  Requirements: xmltodict 

## IMPORT REQUIREMENTS
import xml.etree.cElementTree as ET
import xmltodict

## FUNCTION: CONVERT CHECKLIST (XML) TO DICTIONARY
def convert_ckl_to_dict(RAW_CKL):
    ## CONVERT XML TO PYTHON DICTIONARY
    CHECKLIST_DICT = xmltodict.parse(RAW_CKL, dict_constructor=dict)

    ## RETURN DICTIONARY
    return CHECKLIST_DICT

## FUNCTION: GENERATE STIG INFO ELEMENTS
def generate_stig_info(PARENT, KEY, VALUE):
    SI_DATA = ET.SubElement(PARENT, 'SI_DATA')
    SID_NAME = ET.SubElement(SI_DATA, 'SID_NAME').text = KEY

    if VALUE != None:
        SID_DATA = ET.SubElement(SI_DATA, 'SID_DATA').text = VALUE

## FUNCTION: GENERATE VULN ELEMENTS
def generate_vuln(PARENT, KEY, VALUE):
    STIG_DATA = ET.SubElement(PARENT, 'STIG_DATA')
    VULN_ATTRIBUTE = ET.SubElement(STIG_DATA, 'VULN_ATTRIBUTE').text = KEY
    ATTRIBUTE_DATA = ET.SubElement(STIG_DATA, 'ATTRIBUTE_DATA').text = VALUE

## FUNCTION: FIND BETWEEN TWO POINTS IN A STRING
## NEEDED DUE TO XML TAGS BEING CONTAINED WITHIN DESCRIPTION TEXT
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


## FUNCTION: PRETTY PRINT ELEMENTTREE OUTPUT
## THIS IS NOT NEEDED AS OF NOW
## TO USE, CALL FUNCTION
##      PrettyPrint(ElementTree_Object)
def PrettyPrint(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            PrettyPrint(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem 
