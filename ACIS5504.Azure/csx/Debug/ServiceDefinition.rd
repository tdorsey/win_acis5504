<?xml version="1.0" encoding="utf-8"?>
<serviceModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" name="ACIS5504.Azure" generation="1" functional="0" release="0" Id="41d0f31e-9d0f-4daa-9cad-a39cfdb21006" dslVersion="1.2.0.0" xmlns="http://schemas.microsoft.com/dsltools/RDSM">
  <groups>
    <group name="ACIS5504.AzureGroup" generation="1" functional="0" release="0">
      <componentports>
        <inPort name="ACIS5504:Endpoint1" protocol="http">
          <inToChannel>
            <lBChannelMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/LB:ACIS5504:Endpoint1" />
          </inToChannel>
        </inPort>
      </componentports>
      <settings>
        <aCS name="ACIS5504:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="">
          <maps>
            <mapMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/MapACIS5504:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </maps>
        </aCS>
        <aCS name="ACIS5504Instances" defaultValue="[1,1,1]">
          <maps>
            <mapMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/MapACIS5504Instances" />
          </maps>
        </aCS>
      </settings>
      <channels>
        <lBChannel name="LB:ACIS5504:Endpoint1">
          <toPorts>
            <inPortMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504/Endpoint1" />
          </toPorts>
        </lBChannel>
      </channels>
      <maps>
        <map name="MapACIS5504:Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" kind="Identity">
          <setting>
            <aCSMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504/Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" />
          </setting>
        </map>
        <map name="MapACIS5504Instances" kind="Identity">
          <setting>
            <sCSPolicyIDMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504Instances" />
          </setting>
        </map>
      </maps>
      <components>
        <groupHascomponents>
          <role name="ACIS5504" generation="1" functional="0" release="0" software="X:\ACIS5504\ACIS5504.Azure\csx\Debug\roles\ACIS5504" entryPoint="base\x64\WaHostBootstrapper.exe" parameters="base\x64\WaIISHost.exe " memIndex="1792" hostingEnvironment="frontendadmin" hostingEnvironmentVersion="2">
            <componentports>
              <inPort name="Endpoint1" protocol="http" portRanges="80" />
            </componentports>
            <settings>
              <aCS name="Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString" defaultValue="" />
              <aCS name="__ModelData" defaultValue="&lt;m role=&quot;ACIS5504&quot; xmlns=&quot;urn:azure:m:v1&quot;&gt;&lt;r name=&quot;ACIS5504&quot;&gt;&lt;e name=&quot;Endpoint1&quot; /&gt;&lt;/r&gt;&lt;/m&gt;" />
            </settings>
            <resourcereferences>
              <resourceReference name="DiagnosticStore" defaultAmount="[4096,4096,4096]" defaultSticky="true" kind="Directory" />
              <resourceReference name="EventStore" defaultAmount="[1000,1000,1000]" defaultSticky="false" kind="LogStore" />
            </resourcereferences>
          </role>
          <sCSPolicy>
            <sCSPolicyIDMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504Instances" />
            <sCSPolicyUpdateDomainMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504UpgradeDomains" />
            <sCSPolicyFaultDomainMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504FaultDomains" />
          </sCSPolicy>
        </groupHascomponents>
      </components>
      <sCSPolicy>
        <sCSPolicyUpdateDomain name="ACIS5504UpgradeDomains" defaultPolicy="[5,5,5]" />
        <sCSPolicyFaultDomain name="ACIS5504FaultDomains" defaultPolicy="[2,2,2]" />
        <sCSPolicyID name="ACIS5504Instances" defaultPolicy="[1,1,1]" />
      </sCSPolicy>
    </group>
  </groups>
  <implements>
    <implementation Id="1397384a-79c7-4c1b-8571-2fb32d42f261" ref="Microsoft.RedDog.Contract\ServiceContract\ACIS5504.AzureContract@ServiceDefinition">
      <interfacereferences>
        <interfaceReference Id="118fd8f8-d880-4369-8fff-7a3317db1ce0" ref="Microsoft.RedDog.Contract\Interface\ACIS5504:Endpoint1@ServiceDefinition">
          <inPort>
            <inPortMoniker name="/ACIS5504.Azure/ACIS5504.AzureGroup/ACIS5504:Endpoint1" />
          </inPort>
        </interfaceReference>
      </interfacereferences>
    </implementation>
  </implements>
</serviceModel>