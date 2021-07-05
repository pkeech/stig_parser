##  ===================================
##  ===== STIG PARSER TEST SCRIPT =====
##  ===================================

##  Created By  : Peter Keech
##  Email       : peter.a.keech@gmail.com
##  Version     : TEST
##  Description : Test Creation of Blank CKL File
##  Requirements: n/a 


## IMPORT REQUIREMENTS
from xml.dom import minidom
import os

##  ---------------------
##  ----- FUNCTIONS -----
##  ---------------------

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

##  -----------------------------
##  ----- DEFINE XML OBJECT -----
##  -----------------------------

## DEFINE XML ROOT
root = minidom.Document()

## DEFINE XML
xml = root.createElement('CHECKLIST')

## ADD 'ROOT' TO XML OBJECT
root.appendChild(xml)

## CREATE COMMENT LINE
comment = root.createComment('DISA STIG Viewer :: 2.14')
root.appendChild(comment)

##  --------------------------
##  ----- ASSET ELEMENTS -----
##  --------------------------

## CREATE ASSET ELEMENT 
asset_element = create_element('ASSET', '', xml)

## ADD ASSET ELEMENTS
create_element("ROLE", "None", asset_element)                    ## ASSET ROLE 
create_element("ASSET_TYPE", "Computing", asset_element)         ## ASSET TYPE 
create_element("HOST_NAME", "Test Hostname", asset_element)      ## ASSET HOSTNAME 
create_element("HOST_IP", "1.1.1.1", asset_element)              ## ASSET IP 
create_element("HOST_MAC", "0A:0A:0A:0A:0A", asset_element)      ## ASSET MAC ADDRESS 
create_element("HOST_FQDN", "test.hostname.dev", asset_element)  ## ASSET FQDN 
create_element("TARGET_COMMENT", "", asset_element)              ## ASSET TARGET COMMENT 
create_element("TECH_AREA", "", asset_element)                   ## ASSET TECH AREA 
create_element("TARGET_KEY", "3425", asset_element)              ## ASSET TARGET KEY 
create_element("WEB_OR_DATABASE", "false", asset_element)        ## ASSET WEB OR DATABASE 
create_element("WEB_DB_SITE", "", asset_element)                 ## ASSET DB SITE 
create_element("WEB_DB_INSTANCE", "", asset_element)             ## ASSET DB INSTANCE

##  -------------------------
##  ----- STIG ELEMENTS -----
##  -------------------------

## CREATE STIG ELEMENTS
stig_element = create_element('STIGS', '', xml)
istig_element = create_element('iSTIG', '', stig_element)
stiginfo_element = create_element('STIG_INFO', '', istig_element)

##  ------------------------------
##  ----- STIG INFO ELEMENTS -----
##  ------------------------------

## DEBUG: STATIC ENTRIES FOR TESTING PURPOSES
DESCRIP = "This Security Technical Implementation Guide is published as a tool to improve the security of Department of Defense (DoD) information systems. The requirements are derived from the National Institute of Standards and Technology (NIST) 800-53 and related documents. Comments or proposed revisions to this document should be sent via email to the following address: disa.stig_spt@mail.mil."
FILENAME = "U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml"
TITLE = "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide"

## CREATE SI DATA (VERSION)
create_two_elements_parent('SID_NAME', 'version', 'SID_DATA', '1', 'SI_DATA', stiginfo_element)                                             ## STIG VERSION
create_two_elements_parent('SID_NAME', 'classification', 'SID_DATA', 'UNCLASSIFIED', 'SI_DATA', stiginfo_element)                           ## STIG CLASSIFICATION
create_two_elements_parent('SID_NAME', 'customname', 'SID_DATA', '', 'SI_DATA', stiginfo_element)                                           ## STIG CUSTOMNAME
create_two_elements_parent('SID_NAME', 'stigid', 'SID_DATA', 'Docker_Enterprise_2-x_Linux-UNIX_STIG', 'SI_DATA', stiginfo_element)          ## STIG ID
create_two_elements_parent('SID_NAME', 'description', 'SID_DATA', DESCRIP, 'SI_DATA', stiginfo_element)                                     ## STIG DESCRIPTION
create_two_elements_parent('SID_NAME', 'filename', 'SID_DATA', FILENAME, 'SI_DATA', stiginfo_element)                                       ## STIG FILENAME
create_two_elements_parent('SID_NAME', 'releaseinfo', 'SID_DATA', 'Release: 1 Benchmark Date: 19 Jul 2019', 'SI_DATA', stiginfo_element)    ## STIG RELEASE INFO
create_two_elements_parent('SID_NAME', 'title', 'SID_DATA', TITLE, 'SI_DATA', stiginfo_element)                                             ## STIG TITLE
create_two_elements_parent('SID_NAME', 'uuid', 'SID_DATA', 'eaab6cca-d77d-4787-868b-766afc44845d', 'SI_DATA', stiginfo_element)             ## STIG UUID
create_two_elements_parent('SID_NAME', 'notice', 'SID_DATA', 'terms-of-use', 'SI_DATA', stiginfo_element)                                   ## STIG NOTICE
create_two_elements_parent('SID_NAME', 'source', 'SID_DATA', '', 'SI_DATA', stiginfo_element)                                               ## STIG SOURCE

##  --------------------------
##  ----- VULNS ELEMENTS -----
##  --------------------------

## CREATE VULN ELEMENT
vuln_element = create_element('VULN', '', istig_element)

## DEBUG: STATIC ENTRIES FOR TESTING PURPOSES
RULE_TITLE = "The Docker Enterprise Per User Limit Login Session Control in the Universal Control Plane (UCP) Admin Settings must be set to an organization-defined value for all accounts and/or account types."
DISCUSSION = "The UCP component of Docker Enterprise includes a built-in access authorization mechanism called eNZi which can be integrated with an LDAP server and subsequently configured to limit the number of concurrent sessions to an organization-defined number for all accounts and/or account types. Per-user session control limits are configured with a default of 10. For reference, the per user limit in UCP specifies the maximum number of sessions that any user can have active at any given time. If creating a new session would put a user over this limit then the least recently used session will be deleted. A value of zero disables limiting the number of sessions that users may have. This configuration applies to both the UCP and DTR management consoles."
CHECK = '''Check that the "Per User Limit" Login Session Control in the UCP Admin Settings is set according to the values defined in the System Security Plan.

						via UI:

						In the UCP web console, navigate to "Admin Settings" | "Authentication &amp; Authorization" and verify the "Per User Limit" field is set according to the number specified in the System Security Plan.

						via CLI:

						Linux (requires curl and jq): As a Docker EE Admin, execute the following commands from a machine with connectivity to the UCP management console. Replace [ucp_url] with the UCP URL, [ucp_username] with the username of a UCP administrator and [ucp_password] with the password of a UCP administrator.

						AUTHTOKEN=$(curl -sk -d '{"username":"[ucp_username]","password":"[ucp_password]"}' https://[ucp_url]/auth/login | jq -r .auth_token)
						curl -sk -H "Authorization: Bearer $AUTHTOKEN" https://[ucp_url]/api/ucp/config-toml|grep per_user_limit

						If the "per_user_limit" entry under the "[auth.sessions]" section in the output is not set according to the value defined in the SSP, this is a finding.
'''
FIX = '''Set the "Per User Limit" Login Session Control in the UCP Admin Settings per the requirements set forth by the System Security Plan (SSP).

						via UI:

						In the UCP web console, navigate to "Admin Settings" | "Authentication &amp; Authorization" and set the "Per User Limit" field according to the requirements of this control.

						via CLI:

						Linux (requires curl and jq): As a Docker EE Admin, execute the following commands on either a UCP Manager node or using a UCP client bundle. Replace [ucp_url] with the UCP URL, [ucp_username] with the username of a UCP administrator and [ucp_password] with the password of a UCP administrator.

						AUTHTOKEN=$(curl -sk -d '{"username":"[ucp_username]","password":"[ucp_password]"}' https://[ucp_url]/auth/login | jq -r .auth_token)
						curl -sk -H "Authorization: Bearer $AUTHTOKEN" https://[ucp_url]/api/ucp/config-toml &gt; ucp-config.toml

						Open the "ucp-config.toml" file, set the "per_user_limit" entry under the "[auth.sessions]" section according to the requirements of this control. Save the file.

						Execute the following commands to update UCP with the new configuration:

						curl -sk -H "Authorization: Bearer $AUTHTOKEN" --upload-file ucp-config.toml https://[ucp_url]/api/ucp/config-toml
'''
STIG = "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide :: Version 1, Release: 1 Benchmark Date: 19 Jul 2019"
FINDING_DETAILS = '''Test Finding Details.

					This has been set to "Not a Finding"
'''
STIG_UUID = '9dc3babd-6054-4e33-a4e8-a939ec0b2fc8'

## CREATE VULNERABILITY ELEMENTS
create_two_elements_parent('VULN_ATTRIBUTE', 'Vuln_Num', 'ATTRIBUTE_DATA', 'V-94863', 'STIG_DATA', vuln_element)                ## VULNERABILITY NUMBER
create_two_elements_parent('VULN_ATTRIBUTE', 'Severity', 'ATTRIBUTE_DATA', 'low', 'STIG_DATA', vuln_element)                    ## VULNERABILITY SEVERITY
create_two_elements_parent('VULN_ATTRIBUTE', 'Group_Title', 'ATTRIBUTE_DATA', 'SRG-APP-000001', 'STIG_DATA', vuln_element)      ## VULNERABILITY GROUP TITLE
create_two_elements_parent('VULN_ATTRIBUTE', 'Rule_ID', 'ATTRIBUTE_DATA', 'SV-104693r1_rule', 'STIG_DATA', vuln_element)        ## VULNERABILITY RULE ID
create_two_elements_parent('VULN_ATTRIBUTE', 'Rule_Ver', 'ATTRIBUTE_DATA', 'DKER-EE-001000', 'STIG_DATA', vuln_element)         ## VULNERABILITY RULE VERSION
create_two_elements_parent('VULN_ATTRIBUTE', 'Rule_Title', 'ATTRIBUTE_DATA', RULE_TITLE, 'STIG_DATA', vuln_element)             ## VULNERABILITY RULE TITLE
create_two_elements_parent('VULN_ATTRIBUTE', 'Vuln_Discuss', 'ATTRIBUTE_DATA', DISCUSSION, 'STIG_DATA', vuln_element)           ## VULNERABILITY DISCUSSION
create_two_elements_parent('VULN_ATTRIBUTE', 'IA_Controls', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                    ## VULNERABILITY IA CONTROL
create_two_elements_parent('VULN_ATTRIBUTE', 'Check_Content', 'ATTRIBUTE_DATA', CHECK, 'STIG_DATA', vuln_element)               ## VULNERABILITY CHECK CONTENT
create_two_elements_parent('VULN_ATTRIBUTE', 'Fix_Text', 'ATTRIBUTE_DATA', FIX, 'STIG_DATA', vuln_element)                      ## VULNERABILITY FIX TEXT
create_two_elements_parent('VULN_ATTRIBUTE', 'False_Positives', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                ## VULNERABILITY FALSE POSITIVIES
create_two_elements_parent('VULN_ATTRIBUTE', 'False_Negatives', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                ## VULNERABILITY FALSE NEGATIVES
create_two_elements_parent('VULN_ATTRIBUTE', 'Documentable', 'ATTRIBUTE_DATA', 'false', 'STIG_DATA', vuln_element)              ## VULNERABILITY DOCUMENTABLE
create_two_elements_parent('VULN_ATTRIBUTE', 'Mitigations', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                    ## VULNERABILITY MITIGATION
create_two_elements_parent('VULN_ATTRIBUTE', 'Potential_Impact', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)               ## VULNERABILITY POTENTIAL IMPACT
create_two_elements_parent('VULN_ATTRIBUTE', 'Third_Party_Tools', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)              ## VULNERABILITY THIRD PARTY TOOLS
create_two_elements_parent('VULN_ATTRIBUTE', 'Mitigation_Control', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)             ## VULNERABILITY MITIGATION CONTROLS
create_two_elements_parent('VULN_ATTRIBUTE', 'Responsibility', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                 ## VULNERABILITY RESPONSIBILITY
create_two_elements_parent('VULN_ATTRIBUTE', 'Security_Override_Guidance', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)     ## VULNERABILITY SECURITY OVERRIDE GUIDE
create_two_elements_parent('VULN_ATTRIBUTE', 'Check_Content_Ref', 'ATTRIBUTE_DATA', 'M', 'STIG_DATA', vuln_element)             ## VULNERABILITY CHECK CONTENT REFERENCE
create_two_elements_parent('VULN_ATTRIBUTE', 'Weight', 'ATTRIBUTE_DATA', '10.0', 'STIG_DATA', vuln_element)                     ## VULNERABILITY WEIGHT
create_two_elements_parent('VULN_ATTRIBUTE', 'Class', 'ATTRIBUTE_DATA', 'Unclass', 'STIG_DATA', vuln_element)                   ## VULNERABILITY CLASSIFICATION
create_two_elements_parent('VULN_ATTRIBUTE', 'STIGRef', 'ATTRIBUTE_DATA', STIG, 'STIG_DATA', vuln_element)                      ## VULNERABILITY STIG REFERENCE
create_two_elements_parent('VULN_ATTRIBUTE', 'TargetKey', 'ATTRIBUTE_DATA', '3425', 'STIG_DATA', vuln_element)                  ## VULNERABILITY TARGET KEY
create_two_elements_parent('VULN_ATTRIBUTE', 'STIG_UUID', 'ATTRIBUTE_DATA', STIG_UUID, 'STIG_DATA', vuln_element)               ## VULNERABILITY UUID
create_two_elements_parent('VULN_ATTRIBUTE', 'LEGACY_ID', 'ATTRIBUTE_DATA', '', 'STIG_DATA', vuln_element)                      ## VULNERABILITY LEGACY ID
create_two_elements_parent('VULN_ATTRIBUTE', 'CCI_REF', 'ATTRIBUTE_DATA', 'CCI-000054', 'STIG_DATA', vuln_element)              ## VULNERABILITY CCI REFERENCE

create_element('STATUS', "NotAFinding", vuln_element)                   ## VULNERABILITY FINDING STATUS
create_element('FINDING_DETAILS', FINDING_DETAILS, vuln_element)        ## VULNERABILITY FINDING DETAILS
create_element('COMMENTS', "This are my test comments", vuln_element)   ## VULNERABILITY COMMENTS
create_element('SEVERITY_OVERRIDE', "", vuln_element)                   ## VULNERABILITY SEVERITY OVERRIDE
create_element('SEVERITY_JUSTIFICATION', "", vuln_element)              ## VULNERABILITY SEVERITY JUSTIFICATION

##  -----------------------------
##  ----- GENERATE XML FILE -----
##  -----------------------------

## FORMAT XML
xml_str = root.toprettyxml(indent ="\t", encoding="utf-8") 

## DEFINE SAVE FILE
save_path_file = "test.ckl"

## SAVE XML OBJECT TO FILE
with open(save_path_file, "wb") as f:
    f.write(xml_str)

## DEBUG
print("XML FILE CREATED SUCCESSFULLY!")