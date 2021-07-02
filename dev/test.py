## IMPORT REQUIREMENTS

## LOAD REQUIREMENTS
from xml.dom import minidom
import os

## DEFINE XML ROOT
root = minidom.Document()

## DEFINE XML
xml = root.createElement('CHECKLIST')

## ADD 'ROOT' TO XML OBJECT
root.appendChild(xml)

## CREATE COMMENT LINE
comment = root.createComment('DISA STIG Viewer :: 2.14')
root.appendChild(comment)

##  ---------------------
##  ----- FUNCTIONS -----
##  ---------------------

## FUNCTION: Create Asset Data 
def add_asset_data(Key, Value, Parent):
    asset_role = root.createElement(Key)
    asset_role_value = root.createTextNode(Value)
    asset_role.appendChild(asset_role_value)
    Parent.appendChild(asset_role)


## FUNCTION: Create STIG Info Data
def add_stig_info_data(Key, Value, Parent):
    sidata = root.createElement('SI_DATA')

    sidata_name = root.createElement('SID_NAME')
    sidata_name_value = root.createTextNode(Key)
    sidata_name.appendChild(sidata_name_value)
    sidata.appendChild(sidata_name)

    if Value != " ":
        sidata_data = root.createElement('SID_DATA')
        sidata_data_value = root.createTextNode(Value)
        sidata_data.appendChild(sidata_data_value)
        sidata.appendChild(sidata_data)

    Parent.appendChild(sidata)

## FUNCTION: Create Vulnerability Info
def add_vuln_info_data(Key, Value, Parent):
    vulnData = root.createElement('STIG_DATA')

    vulnData_name = root.createElement('VULN_ATTRIBUTE')
    vulnData_name_value = root.createTextNode(Key)
    vulnData_name.appendChild(vulnData_name_value)
    vulnData.appendChild(vulnData_name)

    #if Value != " ":
    vulnData_data = root.createElement('ATTRIBUTE_DATA')
    vulnData_data_value = root.createTextNode(Value)
    vulnData_data.appendChild(vulnData_data_value)
    vulnData.appendChild(vulnData_data)

    Parent.appendChild(vulnData)

    
##  --------------------------
##  ----- ASSET ELEMENTS -----
##  --------------------------

## CREATE ASSET ELEMENT 
## <ASSET></ASSET>
asset_object = root.createElement('ASSET')
xml.appendChild(asset_object)

## ADD ASSET ELEMENTS
add_asset_data("ROLE", "None", asset_object)                    ## ASSET ROLE 
add_asset_data("ASSET_TYPE", "Computing", asset_object)         ## ASSET TYPE 
add_asset_data("HOST_NAME", "Test Hostname", asset_object)      ## ASSET HOSTNAME 
add_asset_data("HOST_IP", "1.1.1.1", asset_object)              ## ASSET IP 
add_asset_data("HOST_MAC", "0A:0A:0A:0A:0A", asset_object)      ## ASSET MAC ADDRESS 
add_asset_data("HOST_FQDN", "test.hostname.dev", asset_object)  ## ASSET FQDN 
add_asset_data("TARGET_COMMENT", " ", asset_object)             ## ASSET TARGET COMMENT 
add_asset_data("TECH_AREA", " ", asset_object)                  ## ASSET TECH AREA 
add_asset_data("TARGET_KEY", "3425", asset_object)              ## ASSET TARGET KEY 
add_asset_data("WEB_OR_DATABASE", "false", asset_object)        ## ASSET WEB OR DATABASE 
add_asset_data("WEB_DB_SITE", " ", asset_object)                ## ASSET DB SITE 
add_asset_data("WEB_DB_INSTANCE", " ", asset_object)            ## ASSET DB INSTANCE

##  -------------------------
##  ----- STIG ELEMENTS -----
##  -------------------------

## CREATE STIG ELEMENT
## <ASSET></ASSET>
stig_object = root.createElement('STIGS')
xml.appendChild(stig_object)

## CREATE iSTIG ELEMENT
istig_object = root.createElement('iSTIG')
stig_object.appendChild(istig_object)

## CREATE STIG_INFO ELEMENT
stig_info_object = root.createElement('STIG_INFO')
istig_object.appendChild(stig_info_object)


##  ------------------------------
##  ----- STIG INFO ELEMENTS -----
##  ------------------------------

## DEBUG: DEFINE STIG DESCRIPTION
DESCRIP = "This Security Technical Implementation Guide is published as a tool to improve the security of Department of Defense (DoD) information systems. The requirements are derived from the National Institute of Standards and Technology (NIST) 800-53 and related documents. Comments or proposed revisions to this document should be sent via email to the following address: disa.stig_spt@mail.mil."
FILENAME = "U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml"
TITLE = "Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide"

## CREATE SI DATA (VERSION)
add_stig_info_data("version", "1", stig_info_object)                                            ## STIG VERSION
add_stig_info_data("classification", "UNCLASSIFIED", stig_info_object)                          ## STIG CLASSIFICATION
add_stig_info_data("customname", " ", stig_info_object)                                         ## STIG CUSTOMNAME
add_stig_info_data("stigid", "Docker_Enterprise_2-x_Linux-UNIX_STIG", stig_info_object)         ## STIG ID
add_stig_info_data("description", DESCRIP, stig_info_object)                                    ## STIG DESCRIPTION
add_stig_info_data("filename", FILENAME, stig_info_object)                                      ## STIG FILENAME
add_stig_info_data("releaseinfo", "Release: 1 Benchmark Date: 19 Jul 2019", stig_info_object)   ## STIG RELEASE INFO
add_stig_info_data("title", TITLE, stig_info_object)                                            ## STIG TITLE
add_stig_info_data("uuid", "eaab6cca-d77d-4787-868b-766afc44845d", stig_info_object)            ## STIG UUID
add_stig_info_data("notice", "terms-of-use", stig_info_object)                                  ## STIG NOTICE
add_stig_info_data("source", " ", stig_info_object)                                             ## STIG SOURCE

##  --------------------------
##  ----- VULNS ELEMENTS -----
##  --------------------------

## CREATE VULN ELEMENT
stig_info_object = root.createElement('VULN')
istig_object.appendChild(stig_info_object)

## DEBUG
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

## CREATE STIG_DATA ELEMENTS
add_vuln_info_data("Vuln_Num", "V-94863", stig_info_object)                                 ## VULNERABILITY NUMBER
add_vuln_info_data("Severity", "low", stig_info_object)                                     ## VULNERABILITY SEVERITY
add_vuln_info_data("Group_Title", "SRG-APP-000001", stig_info_object)                       ## VULNERABILITY GROUP TITLE
add_vuln_info_data("Rule_ID", "SV-104693r1_rule", stig_info_object)                         ## VULNERABILITY RULE ID
add_vuln_info_data("Rule_Ver", "DKER-EE-001000", stig_info_object)                          ## VULNERABILITY RULE VERSION
add_vuln_info_data("Rule_Title", RULE_TITLE, stig_info_object)                              ## VULNERABILITY RULE TITLE
add_vuln_info_data("Vuln_Discuss", DISCUSSION, stig_info_object)                            ## VULNERABILITY DISCUSSION
add_vuln_info_data("IA_Controls", " ", stig_info_object)                                    ## VULNERABILITY IA CONTROL
add_vuln_info_data("Check_Content", CHECK, stig_info_object)                                ## VULNERABILITY CHECK CONTENT
add_vuln_info_data("Fix_Text", FIX, stig_info_object)                                       ## VULNERABILITY FIX TEXT
add_vuln_info_data("False_Positives", " ", stig_info_object)                                ## VULNERABILITY FALSE POSITIVES
add_vuln_info_data("False_Negatives", " ", stig_info_object)                                ## VULNERABILITY FALSE NEGATIVES
add_vuln_info_data("Documentable", "false", stig_info_object)                               ## VULNERABILITY DOCUMENTABLE
add_vuln_info_data("Mitigations", " ", stig_info_object)                                    ## VULNERABILITY MITIGATION
add_vuln_info_data("Potential_Impact", " ", stig_info_object)                               ## VULNERABILITY POTENTIAL IMPACT
add_vuln_info_data("Third_Party_Tools", " ", stig_info_object)                              ## VULNERABILITY THIRD PARTY TOOLS
add_vuln_info_data("Mitigation_Control", " ", stig_info_object)                             ## VULNERABILITY MITIGATION TOOLS
add_vuln_info_data("Responsibility", " ", stig_info_object)                                 ## VULNERABILITY RESPONSIBILITY
add_vuln_info_data("Security_Override_Guidance", " ", stig_info_object)                     ## VULNERABILITY SECURITY OVERRIDE GUIDE
add_vuln_info_data("Check_Content_Ref", "M", stig_info_object)                              ## VULNERABILITY CHECK CONTENT REFERENCE
add_vuln_info_data("Weight", "10.0", stig_info_object)                                      ## VULNERABILITY WEIGHT
add_vuln_info_data("Class", "Unclass", stig_info_object)                                    ## VULNERABILITY CLASSIFICATION
add_vuln_info_data("STIGRef", STIG, stig_info_object)                                       ## VULNERABILITY STIG REFERENCE
add_vuln_info_data("TargetKey", "3425", stig_info_object)                                   ## VULNERABILITY TARGET KEY
add_vuln_info_data("STIG_UUID", "9dc3babd-6054-4e33-a4e8-a939ec0b2fc8", stig_info_object)   ## VULNERABILITY UUID
add_vuln_info_data("LEGACY_ID", " ", stig_info_object)                                      ## VULNERABILITY LEGACY ID
add_vuln_info_data("CCI_REF", "CCI-000054", stig_info_object)                               ## VULNERABILITY CCI REFERENCE

## STATUS
vuln_status = root.createElement('STATUS')
vuln_status_value = root.createTextNode("NotAFinding")
vuln_status.appendChild(vuln_status_value)
stig_info_object.appendChild(vuln_status)

## FINDING DETAILS
FINDING_DETAILS = '''Test Finding Details.

					This has been set to "Not a Finding"
'''

vuln_finding = root.createElement('FINDING_DETAILS')
vuln_finding_value = root.createTextNode(FINDING_DETAILS)
vuln_finding.appendChild(vuln_finding_value)
stig_info_object.appendChild(vuln_finding)

## COMMENTS
vuln_comments = root.createElement('COMMENTS')
vuln_comments_value = root.createTextNode("This are my test comments")
vuln_comments.appendChild(vuln_comments_value)
stig_info_object.appendChild(vuln_comments)

## SEVERITY OVERRIDE
vuln_override = root.createElement('SEVERITY_OVERRIDE')
vuln_override_value = root.createTextNode(" ")
vuln_override.appendChild(vuln_override_value)
stig_info_object.appendChild(vuln_override)

## SERVERITY JUSTIFICATION
vuln_justify = root.createElement('SEVERITY_JUSTIFICATION')
vuln_justify_value = root.createTextNode(" ")
vuln_justify.appendChild(vuln_justify_value)
stig_info_object.appendChild(vuln_justify)













## FORMAT XML
#xml_str = root.toprettyxml(indent ="\t", encoding="utf-8") 

## DEFINE SAVE FILE
save_path_file = "test.ckl"

## SAVE XML OBJECT TO FILE
with open(save_path_file, "wb") as f:
    #f.write(xml_str)
    f.write(root.toprettyxml(indent ="\t", encoding="utf-8"))

## DEBUG
print("XML FILE CREATED SUCCESSFULLY!")