##  ===========================================
##  ===== STIG PARSER CHECKLIST FUNCTIONS =====
##  ===========================================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : 1.0
##  Description : Functions Utilized to create blank Checklists (CKL)
##  Requirements: test2.py

## IMPORT REQUIREMENTS
from xml.dom import minidom
import os, uuid, json

##  ---------------------------
##  ----- CHECKLIST CLASS -----
##  ---------------------------

## DEBUG
#class ComplexEncoder(json.JSONEncoder):
    #def default(self, obj):
        #if hasattr(obj,'toJSON'):
            #return obj.toJSON()
        #else:
            #return json.JSONEncoder.default(self, obj)

## CLASS: STIG Checklist Asset Target Class
class Checklist_Asset_Target:
    ## CREATE EMPTY INSTANCE ON CREATION
    def __init__(self):
        ## DEFINE ATTRIBUTES
        self.area = None
        self.key = None

    ## GENERATE JSON OBJECT OF CLASS
    #def toJSON(self):
        ## RETURN RAW JSON
        #return self.__dict__

## CLASS: STIG Checklist Asset Database Class
class Checklist_Asset_DB:
    ## CREATE EMPTY INSTANCE ON CREATION
    def __init__(self):
        ## DEFINE ATTRIBUTES
        self.site = None
        self.instance = None

    ## GENERATE JSON OBJECT OF CLASS
    #def toJSON(self):
        ## RETURN RAW JSON
        #return self.__dict__

## CLASS: STIG Checklist STIG Class
class Checklist_STIG:
    ## CREATE EMPTY INSTANCE ON CREATION
    def __init__(self):
        ## DEFINE ATTRIBUTES
        self.version = None
        self.classification = None
        self.customname = None
        self.id = None
        self.description = None
        self.filename = None
        self.releaseinfo = None
        self.title = None
        self.uuid = None
        self.notice = None
        self.source = None

    ## GENERATE JSON OBJECT OF CLASS
    #def toJSON(self):
        ### RETURN RAW JSON
        #return self.__dict__

## CLASS: STIG Checklist Class
class Checklist:
    ## CREATE EMPTY INSTANCE ON CREATION
    def __init__(self):
        ## DEFINE ASSET ATTRIBUTES
        self.role = None
        self.type = None
        self.name = "TESTER"
        self.ip = None
        self.mac = None
        self.fqdn = None
        self.comments = None
        self.target = Checklist_Asset_Target()
        self.web_db = None
        self.db = Checklist_Asset_DB()
        self.stig = Checklist_STIG()

    ## GENERATE CHECKLIST FILE
    def printname(output_file, self):
        pass

    ## GENERATE JSON OBJECT OF CHECKLIST
    #def toJSON(self):
        ## GENERATE FORMATTED JSON
        #PRETTY_JSON = json.dumps(self.toJSON(), indent=4, cls=ComplexEncoder)

        ## RETURN PRETTY JSON
        #return PRETTY_JSON


##  -----------------------------
##  ----- PRIVATE FUNCTIONS -----
##  -----------------------------

## FUNCTION: Create Element
def create_element(Key, Value, Parent):
    ## CREATE ELEMENT
    element = root.createElement(Key)

    ## ADD VALUE IF PASSED
    if Value != "":
        element_value = root.createTextNode(Value)
        element.appendChild(element_value)
    
    ## ADD ELEMENT TO PARENT
    Parent.appendChild(element)

    ## RETURN ELEMENT
    return element

## FUNCTION: Create Element w/ Parent
def create_two_elements_parent(Key1, Value1, Key2, Value2, ParentName, GrandParent):
    ## CREATE PARENT ELEMENT
    Parent = create_element(ParentName, '', GrandParent)

    ## CREATE ELEMENTS
    Element1 = create_element(Key1, Value1, Parent)
    Element2 = create_element(Key2, Value2, Parent)

    ## ADD ELEMENTS TO NEW PARENT
    Parent.appendChild(Element1)
    Parent.appendChild(Element2)

    ## RETURN PARENT ELEMENT
    return Parent

##  ----------------------------
##  ----- PUBLIC FUNCTIONS -----
##  ----------------------------

## FUNCTION: Create Empty Checklist
def create_checklist(STIG_JSON, FILENAME):
    ## DEBUG
    newChecklist = Checklist()

    ## MAP STIG VALUES TO CHECKLIST ATTRIBUTES
    newChecklist.stig.version = STIG_JSON['version']
    #newChecklist.stig.classification = STIG_JSON['############']
    newChecklist.stig.customname = ""
    #newChecklist.stig.id = STIG_JSON['############']
    newChecklist.stig.description = STIG_JSON['description']
    newChecklist.stig.filename = (FILENAME.split('/'))[-1]
    newChecklist.stig.releaseinfo = "Release: " + STIG_JSON['release'] + "Benchmark Date: " + STIG_JSON['benchmark_date']
    newChecklist.stig.title = STIG_JSON['title']
    newChecklist.stig.uuid = uuid.uuid4()
    #newChecklist.stig.notice = STIG_JSON['#########']
    #newChecklist.stig.source = STIG_JSON['########']

    ## Fake Values
    newChecklist.name = "Test Class Function"

    ## Return Checklist Object
    return newChecklist
