import pandas as pd
import xml.etree.ElementTree as ET

# Corrected XML input string
xml_string_corrected = """
<Document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:1so:std:1so:20022:tech:xsd:auth.031.001.01 auth.031.001.01_ESMAUG_1.0.0.xsd" xmlns="urn:1so:std:1so:20022:tech:xsd:auth.031.001.01">
    <FinInstrmRptgStsAdvc>
        <StsAdvc>
            <MsgRptIdr>EXAMPLE12352</MsgRptIdr>
            <MsgSts>
                <Sts>ACPT</Sts>
                <MsgDt>2024-08-14</MsgDt>
                <Sttstcs>
                    <Tt1NbOfRcrds>15</Tt1NbOfRcrds>
                    <NbOfRcrdsPerSts>
                        <DtldNbOfRcrds>11</DtldNbOfRcrds>
                        <DtldSts>ACPT</DtldSts>
                    </NbOfRcrdsPerSts>
                    <NbOfRcrdsPerSts>
                        <DtldNbOfRcrds>4</DtldNbOfRcrds>
                        <DtldSts>RJCT</DtldSts>
                    </NbOfRcrdsPerSts>
                </Sttstcs>
            </MsgSts>
            <RcrdSts>
                <Orgn1RcrdId>EUSFALALALSFTRC8728MARGINSC1TC7251975</Orgn1RcrdId>
                <Sts>ACPT</Sts>
                <valid>ACPT</valid>
            </RcrdSts>
        </StsAdvc>
    </FinInstrmRptgStsAdvc>
</Document>
"""

# Function to remove namespace from an element's tag
def strip_namespace(element):
    element.tag = element.tag.split('}')[-1]
    for child in element:
        strip_namespace(child)

# Parse the corrected XML string
root = ET.fromstring(xml_string_corrected)
strip_namespace(root)  # Remove namespaces from the XML

# Extract MsgSts for msgsts_df
msgsts = root.find('.//MsgSts')
msgsts_df = pd.DataFrame({'col1': [1], 'col2': [ET.tostring(msgsts, encoding='unicode')]} if msgsts is not None else [])

# Extract Sttstcs for sttstcs_df
sttstcs = root.find('.//Sttstcs')
sttstcs_df = pd.DataFrame({'col1': [1], 'col2': [ET.tostring(sttstcs, encoding='unicode')]} if sttstcs is not None else [])

# Extract RcrdSts for rcrdsts_df
rcrdsts = root.find('.//RcrdSts')
if rcrdsts is not None:
    orgn_id = rcrdsts.find('Orgn1RcrdId').text if rcrdsts.find('Orgn1RcrdId') is not None else None
    rcrdsts_df = pd.DataFrame({'col1': [1], 'col2': [orgn_id], 'col3': [ET.tostring(rcrdsts, encoding='unicode')]})
else:
    rcrdsts_df = pd.DataFrame()

# Output the dataframes
print("msgsts_df:")
print(msgsts_df)
print("\nsttstcs_df:")
print(sttstcs_df)
print("\nrcrdsts_df:")
print(rcrdsts_df)
