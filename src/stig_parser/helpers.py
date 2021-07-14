##  ==============================
##  ===== STIG PARSER MODULE =====
##  ==============================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Description : Helper File
##  Requirements: n/a  

## IMPORT REQUIREMENTS
from xml.dom import minidom

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
def create_two_elements_parent(KEY1, VALUE1, KEY2, VALUE2, PARENTNAME, GRANDPARENT):
    ## CREATE PARENT ELEMENT
    PARENT = create_element(PARENTNAME, '', GRANDPARENT)

    ## CREATE ELEMENTS
    ELEMENT1 = create_element(KEY1, VALUE1, PARENT)
    ELEMENT2 = create_element(KEY2, VALUE2, PARENT)

    ## ADD ELEMENTS TO NEW PARENT
    PARENT.appendChild(ELEMENT1)
    PARENT.appendChild(ELEMENT2)

    ## RETURN PARENT ELEMENT
    return PARENT
