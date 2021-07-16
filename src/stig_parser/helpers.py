##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Description : Helper File
##  Requirements: xmltodict 

## IMPORT REQUIREMENTS
from xml.dom import minidom
import xmltodict

## FUNCTION: CREATE ELEMENT
def create_element(ROOT, KEY, VALUE, PARENT):
    ## CREATE ELEMENT
    ELEMENT = ROOT.createElement(KEY)

    ## ADD VALUE IF PASSED
    if VALUE != "":
        ELEMENT_VALUE = ROOT.createTextNode(VALUE)
        ELEMENT.appendChild(ELEMENT_VALUE)
    
    ## ADD ELEMENT TO PARENT
    PARENT.appendChild(ELEMENT)

    ## RETURN ELEMENT
    return ELEMENT

## FUNCTION: CREATE TWO ELEMENTS WITH SAME PARENT
def create_two_elements_parent(ROOT, KEY1, VALUE1, KEY2, VALUE2, PARENTNAME, GRANDPARENT):
    ## CREATE PARENT ELEMENT
    PARENT = create_element(ROOT, PARENTNAME, '', GRANDPARENT)

    ## CREATE ELEMENTS
    ELEMENT1 = create_element(ROOT, KEY1, VALUE1, PARENT)
    ELEMENT2 = create_element(ROOT, KEY2, VALUE2, PARENT)

    ## ADD ELEMENTS TO NEW PARENT
    PARENT.appendChild(ELEMENT1)
    PARENT.appendChild(ELEMENT2)

    ## RETURN PARENT ELEMENT
    return PARENT

## FUNCTION: CONVERT CHECKLIST (XML) TO DICTIONARY
def convert_ckl_to_dict(RAW_CKL):
    ## CONVERT XML TO PYTHON DICTIONARY
    CHECKLIST_DICT = xmltodict.parse(RAW_CKL, dict_constructor=dict)

    ## RETURN DICTIONARY
    return CHECKLIST_DICT

## FUNCTION: FIND BETWEEN TWO POINTS IN A STRING
## NEEDED DUE TO XML TAGS BEING CONTAINED WITHIN DESCRIPTION TEXT
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""