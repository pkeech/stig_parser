# CKL to STIG Mappings

### CKL Layout

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<!--DISA STIG Viewer :: 2.14-->
<CHECKLIST>
	<ASSET>
        ...
    </ASSET>
    <STIGS>
        <iSTIG>
            <STIG_INFO>
                ...
            </STIG_INFO>
            <VULN>
                ...
            </VULN>
        </iSTIG>
    </STIGS>
</CHECKLIST>
```



### Asset Breakdown

**Layout**
``` xml
<ASSET>
    <ROLE>None</ROLE>
    <ASSET_TYPE>Computing</ASSET_TYPE>
    <HOST_NAME>Test Hostname</HOST_NAME>
    <HOST_IP>1.1.1.1</HOST_IP>
    <HOST_MAC>0A:0A:0A:0A:0A</HOST_MAC>
    <HOST_FQDN>test.hostname.dev</HOST_FQDN>
    <TARGET_COMMENT></TARGET_COMMENT>
    <TECH_AREA></TECH_AREA>
    <TARGET_KEY>3425</TARGET_KEY>
    <WEB_OR_DATABASE>false</WEB_OR_DATABASE>
    <WEB_DB_SITE></WEB_DB_SITE>
    <WEB_DB_INSTANCE></WEB_DB_INSTANCE>
</ASSET>
```

**Fields**

| Field | CKL FILE | STIG FILE | VALUES |
| :---: | --- | --- | :---: |
| Role | ```<ROLE></ROLE>``` | - | `None`, `Workstation`, `Member Server`, `Domain Controller` |
| Asset Type | ```<ASSET_TYPE></ASSET_TYPE>``` | - | `Computing`, `Non-Computing` |
| Host Name | ```<HOST_NAME></HOST_NAME>``` | - | Free Text |
| Host IP | ```<HOST_IP></HOST_IP>``` | - | Free Text |
| Host MAC | ```<HOST_MAC></HOST_MAC>``` | - | Free Text |
| Host FQDN | ```<HOST_FQDN></HOST_FQDN>``` | - | Free Text |
| Target Comment | ```<TARGET_COMMENT></TARGET_COMMENT>``` | - | Free Text |
| Tech Area | ```<TECH_AREA></TECH_AREA>``` | - | `Application Review`, `Boundary Security`, `CDS Admin Review`, `CDS Technical Review`, `Database Review`, `Domain Name System (DNS)`, `Exchange Server`, `Host Based System Security (HBSS)`, `Internal Network`, `Mobility`, `Releasable Networks (REL)`, `Traditional Security`, `UNIX OS`, `VVOIP Review`, `Web Review`, `Windows OS`, `Other Review` |
| Target Key | ```<TARGET_KEY></TARGET_KEY>``` | - | Free Text |
| Web or DB | ```<WEB_OR_DATABASE></WEB_OR_DATABASE>``` | - | `true`, `false` |
| Web/DB Site | ```<WEB_DB_SITE></WEB_DB_SITE>``` | - | Free Text |
| Web/DB Instance | ```<WEB_DB_INSTANCE></WEB_DB_INSTANCE>``` | - | Free Text |

### STIG Breakdown

**Layout**
``` xml
	<STIGS>
		<iSTIG>
			<STIG_INFO>
				<SI_DATA>
					<SID_NAME>version</SID_NAME>
					<SID_DATA>1</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>classification</SID_NAME>
					<SID_DATA>UNCLASSIFIED</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>customname</SID_NAME>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>stigid</SID_NAME>
					<SID_DATA>Docker_Enterprise_2-x_Linux-UNIX_STIG</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>description</SID_NAME>
					<SID_DATA>This Security Technical Implementation Guide is published as a tool to improve the security of Department of Defense (DoD) information systems. The requirements are derived from the National Institute of Standards and Technology (NIST) 800-53 and related documents. Comments or proposed revisions to this document should be sent via email to the following address: disa.stig_spt@mail.mil.</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>filename</SID_NAME>
					<SID_DATA>U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>releaseinfo</SID_NAME>
					<SID_DATA>Release: 1 Benchmark Date: 19 Jul 2019</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>title</SID_NAME>
					<SID_DATA>Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>uuid</SID_NAME>
					<SID_DATA>eaab6cca-d77d-4787-868b-766afc44845d</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>notice</SID_NAME>
					<SID_DATA>terms-of-use</SID_DATA>
				</SI_DATA>
				<SI_DATA>
					<SID_NAME>source</SID_NAME>
				</SI_DATA>
			</STIG_INFO>
            <VULN>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Vuln_Num</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>V-94863</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Severity</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>low</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Group_Title</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>SRG-APP-000001</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Rule_ID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>SV-104693r1_rule</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Rule_Ver</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>DKER-EE-001000</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Rule_Title</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>The Docker Enterprise Per User Limit Login Session Control in the Universal Control Plane (UCP) Admin Settings must be set to an organization-defined value for all accounts and/or account types.</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Vuln_Discuss</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>The UCP component of Docker Enterprise includes a built-in access authorization mechanism called eNZi which can be integrated with an LDAP server and subsequently configured to limit the number of concurrent sessions to an organization-defined number for all accounts and/or account types. Per-user session control limits are configured with a default of 10. For reference, the per user limit in UCP specifies the maximum number of sessions that any user can have active at any given time. If creating a new session would put a user over this limit then the least recently used session will be deleted. A value of zero disables limiting the number of sessions that users may have. This configuration applies to both the UCP and DTR management consoles.</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>IA_Controls</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Check_Content</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>Check that the "Per User Limit" Login Session Control in the UCP Admin Settings is set according to the values defined in the System Security Plan.

                    via UI:

                    In the UCP web console, navigate to "Admin Settings" | "Authentication &amp; Authorization" and verify the "Per User Limit" field is set according to the number specified in the System Security Plan.

                    via CLI:

                    Linux (requires curl and jq): As a Docker EE Admin, execute the following commands from a machine with connectivity to the UCP management console. Replace [ucp_url] with the UCP URL, [ucp_username] with the username of a UCP administrator and [ucp_password] with the password of a UCP administrator.

                    AUTHTOKEN=$(curl -sk -d '{"username":"[ucp_username]","password":"[ucp_password]"}' https://[ucp_url]/auth/login | jq -r .auth_token)
                    curl -sk -H "Authorization: Bearer $AUTHTOKEN" https://[ucp_url]/api/ucp/config-toml|grep per_user_limit

                    If the "per_user_limit" entry under the "[auth.sessions]" section in the output is not set according to the value defined in the SSP, this is a finding.</ATTRIBUTE_DATA>
                </STIG_DATA>
                <STIG_DATA>
					<VULN_ATTRIBUTE>Fix_Text</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>Set the "Per User Limit" Login Session Control in the UCP Admin Settings per the requirements set forth by the System Security Plan (SSP).

                    via UI:

                    In the UCP web console, navigate to "Admin Settings" | "Authentication &amp; Authorization" and set the "Per User Limit" field according to the requirements of this control.

                    via CLI:

                    Linux (requires curl and jq): As a Docker EE Admin, execute the following commands on either a UCP Manager node or using a UCP client bundle. Replace [ucp_url] with the UCP URL, [ucp_username] with the username of a UCP administrator and [ucp_password] with the password of a UCP administrator.

                    AUTHTOKEN=$(curl -sk -d '{"username":"[ucp_username]","password":"[ucp_password]"}' https://[ucp_url]/auth/login | jq -r .auth_token)
                    curl -sk -H "Authorization: Bearer $AUTHTOKEN" https://[ucp_url]/api/ucp/config-toml &gt; ucp-config.toml

                    Open the "ucp-config.toml" file, set the "per_user_limit" entry under the "[auth.sessions]" section according to the requirements of this control. Save the file.

                    Execute the following commands to update UCP with the new configuration:

                    curl -sk -H "Authorization: Bearer $AUTHTOKEN" --upload-file ucp-config.toml https://[ucp_url]/api/ucp/config-toml</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>False_Positives</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>False_Negatives</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Documentable</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>false</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Mitigations</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Potential_Impact</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Third_Party_Tools</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Mitigation_Control</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Responsibility</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Security_Override_Guidance</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Check_Content_Ref</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>M</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Weight</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>10.0</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>Class</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>Unclass</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>STIGRef</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide :: Version 1, Release: 1 Benchmark Date: 19 Jul 2019</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>TargetKey</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>3425</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>STIG_UUID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>9dc3babd-6054-4e33-a4e8-a939ec0b2fc8</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>LEGACY_ID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>LEGACY_ID</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA></ATTRIBUTE_DATA>
				</STIG_DATA>
				<STIG_DATA>
					<VULN_ATTRIBUTE>CCI_REF</VULN_ATTRIBUTE>
					<ATTRIBUTE_DATA>CCI-000054</ATTRIBUTE_DATA>
				</STIG_DATA>
				<STATUS>NotAFinding</STATUS>
				<FINDING_DETAILS>Test Finding Details.

                    This has been set to "Not a Finding"</FINDING_DETAILS>
				<COMMENTS>This are my test comments</COMMENTS>
				<SEVERITY_OVERRIDE></SEVERITY_OVERRIDE>
				<SEVERITY_JUSTIFICATION></SEVERITY_JUSTIFICATION>
			</VULN>
```

**Fields (STIG Data)**

| Field | CKL FILE | STIG FILE |
| :---: | --- | --- |
| Version | ```<SI_DATA><SID_NAME>version</SID_NAME><SID_DATA>1</SID_DATA></SI_DATA>``` | ```<version>1</version>```|
| Classification | ```<SI_DATA><SID_NAME>classification</SID_NAME><SID_DATA>UNCLASSIFIED</SID_DATA></SI_DATA>```| ??? |
| Custom Name | ```<SI_DATA><SID_NAME>customname</SID_NAME></SI_DATA>``` | ??? |
| STIG ID | ```<SI_DATA><SID_NAME>stigid</SID_NAME><SID_DATA>Docker_Enterprise_2-x_Linux-UNIX_STIG</SID_DATA></SI_DATA>``` | ```<Benchmark id="Docker_Enterprise_2-x_Linux-UNIX_STIG"></Benchmark>``` |
| Description | ```<SI_DATA><SID_NAME>description</SID_NAME><SID_DATA>This Security Technical ...</SID_DATA></SI_DATA>``` | ```<description>This Security Technical Implementation ...></description>``` |
| Filename | ```<SI_DATA><SID_NAME>filename</SID_NAME><SID_DATA>U_Docker_Enterprise_2-x_Linux-UNIX_STIG_V1R1_Manual-xccdf.xml</SID_DATA></SI_DATA>``` | From Passed STIG File |
| Release Info | ```<SI_DATA><SID_NAME>releaseinfo</SID_NAME><SID_DATA>Release: 1 Benchmark Date: 19 Jul 2019</SID_DATA></SI_DATA>``` | ```<plain-text id="release-info">Release: 1 Benchmark Date: 19 Jul 2019</plain-text>``` |
| Title | ```<SI_DATA><SID_NAME>title</SID_NAME><SID_DATA>Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide</SID_DATA></SI_DATA>``` | ```<title>Docker Enterprise 2.x Linux/UNIX Security Technical Implementation Guide</title>``` |
| UUID | ```<SI_DATA><SID_NAME>uuid</SID_NAME><SID_DATA>eaab6cca-d77d-4787-868b-766afc44845d</SID_DATA></SI_DATA>``` | ??? |
| Notice | ```<SI_DATA><SID_NAME>notice</SID_NAME><SID_DATA>terms-of-use</SID_DATA></SI_DATA>``` | ```<notice id="terms-of-use" xml:lang="en"></notice>``` |



**Fields (Vulnerabilities)**

| Field | CKL FILE | STIG FILE |
| :---: | --- | --- |
| Vulnerability Number | ```<STIG_DATA><VULN_ATTRIBUTE>Vuln_Num</VULN_ATTRIBUTE><ATTRIBUTE_DATA>V-94863</ATTRIBUTE_DATA></STIG_DATA>``` | ```<Group id="V-94863">``` |
| Severity | ```<STIG_DATA><VULN_ATTRIBUTE>Severity</VULN_ATTRIBUTE><ATTRIBUTE_DATA>low</ATTRIBUTE_DATA></STIG_DATA>``` | ```<Rule id="SV-104693r1_rule" severity="low" weight="10.0">``` |
| Group Title | ```<STIG_DATA><VULN_ATTRIBUTE>Group_Title</VULN_ATTRIBUTE><ATTRIBUTE_DATA>SRG-APP-000001</ATTRIBUTE_DATA></STIG_DATA>``` | ```<title>SRG-APP-000001</title>``` |
| Rule ID | ```<STIG_DATA><VULN_ATTRIBUTE>Rule_ID</VULN_ATTRIBUTE><ATTRIBUTE_DATA>SV-104693r1_rule</ATTRIBUTE_DATA></STIG_DATA>``` | ```<Rule id="SV-104693r1_rule" severity="low" weight="10.0">``` |
| Rule Version | ```<STIG_DATA><VULN_ATTRIBUTE>Rule_Ver</VULN_ATTRIBUTE><ATTRIBUTE_DATA>DKER-EE-001000</ATTRIBUTE_DATA></STIG_DATA>``` | ```<version>DKER-EE-001000</version>``` |
| Rule Title | ```<STIG_DATA><VULN_ATTRIBUTE>Rule_Title</VULN_ATTRIBUTE><ATTRIBUTE_DATA>The Docker Enterprise ... </ATTRIBUTE_DATA></STIG_DATA>``` | ```<rule><title>The Docker Enterprise ... </title></rule>``` |
| Vulnerability Discussion | ```<STIG_DATA><VULN_ATTRIBUTE>Vuln_Discuss</VULN_ATTRIBUTE><ATTRIBUTE_DATA>The UCP ...</ATTRIBUTE_DATA></STIG_DATA>``` | ```<rule><description>&lt;VulnDiscussion&gt;The UCP ...&lt;/VulnDiscussion&gt;...</description></rule>``` |
| IA Controls | ```<STIG_DATA><VULN_ATTRIBUTE>IA_Controls</VULN_ATTRIBUTE><ATTRIBUTE_DATA></ATTRIBUTE_DATA></STIG_DATA>``` | ```<rule><description>...&lt;IAControls&gt;&lt;/IAControls&gt;</description></rule>``` |
| Check Content | ```<STIG_DATA><VULN_ATTRIBUTE>Check_Content</VULN_ATTRIBUTE><ATTRIBUTE_DATA>Check that the ...></ATTRIBUTE_DATA></STIG_DATA>``` | ```<rule><check system="C-94171r1_chk"><check-content>Check that the ...></check-content></check></rule>``` |
| Fix Text | ```<STIG_DATA><VULN_ATTRIBUTE>Fix_Text</VULN_ATTRIBUTE><ATTRIBUTE_DATA>Set the "Per ...</ATTRIBUTE_DATA></STIG_DATA>``` | ```<rule><fixtext fixref="F-101009r1_fix">Set the "Per ...></fixtext></rule>``` |
| False Positives | ```<STIG_DATA><VULN_ATTRIBUTE>False_Positives</VULN_ATTRIBUTE><ATTRIBUTE_DATA></ATTRIBUTE_DATA></STIG_DATA>``` | ``` ``` |
| False Negatives | ``` ``` | ```<rule><description>...&lt;FalseNegatives&gt;&lt;/FalseNegatives&gt;&lt;...>``` |
| Documentable | ``` ``` | ```<rule><description>...&lt;Documentable&gt;&lt;/Documentable&gt;&lt;...>``` |
| Mitigations | ``` ``` | ``` ``` |
| Potential Impact | ``` ``` | ``` ``` |
| Third Party Tools | ``` ``` | ``` ``` |
| Mitigation Control | ``` ``` | ``` ``` |
| Responsibility | ``` ``` | ``` ``` |
| Security Override Guidance | ``` ``` | ``` ``` |
| Check Content Reference | ``` ``` | ``` ``` |
| Weight | ``` ``` | ``` ``` |
| Classification | ``` ``` | ``` ``` |
| STIG Reference | ``` ``` | ``` ``` |
| Target Key | ``` ``` | ``` ``` |
| STIG UUID | ``` ``` | ``` ``` |
| Legacy ID | ``` ``` | ``` ``` |
| Legacy ID | ``` ``` | ``` ``` |
| CCI Reference | ``` ``` | ``` ``` |
| Status | ``` ``` | ``` ``` |
| Finding Details | ``` ``` | ``` ``` |
| Comments | ``` ``` | ``` ``` |
| Severity Override | ``` ``` | ``` ``` |
| Severity Justification | ``` ``` | ``` ``` |