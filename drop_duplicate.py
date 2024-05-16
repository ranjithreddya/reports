# import csv
# import xml.etree.ElementTree as ET
# import json
# from deepdiff import DeepDiff
# import xmltodict

# from ordered_set import OrderedSet

# xml_src = "/Users/ranjithrreddyabbidi/ranjith/xml1.xml"
# xml_target = "/Users/ranjithrreddyabbidi/ranjith/xml2.xml"
# xml_final_op = f'/Users/ranjithrreddyabbidi/ranjith'
# print("DEBUGGG")
# tree=ET.parse(xml_src)

# root=tree.getroot()

# tree1=ET.parse(xml_target)

# root1=tree1.getroot()
# xmlstr1 = ET.tostring (root, encoding='utf-8', method='xml').decode() 
# xmlstr2 = ET.tostring (root1, encoding='utf-8', method='xml').decode() 

# xmlstr1 = xmlstr1.replace('ns0:','')
# xmlstr2=xmlstr2.replace('ns0:','')

# print("DEBUGGG")

# # def serialize(obj):
# #     if isinstance(obj, OrderedSet):
# #         return list(obj)
# #     elif isinstance(obj, dict):
# #         return {key: serialize(value) for key, value in obj.items()}
# #     elif isinstance(obj, (list, tuple)):
# #         return [serialize(item) for item in obj]
# #     return obj


# def serialize(obj):
#     if isinstance(obj, OrderedSet):
#         return list(obj)
#     elif isinstance(obj, dict):
#         return {key: serialize(value) for key, value in obj.items()}
#     elif isinstance(obj, (list, tuple)):
#         return [serialize(item) for item in obj]
#     elif isinstance(obj, ET.Element):
#         return element_to_dict(obj)
#     return obj

# def element_to_dict(element):
#     data = {'tagname': element.tag}
#     if element.attrib:
#         data['attributes'] = element.attrib
#     if element.text and element.text.strip():
#         data['text'] = element.text.strip()
#     if element.tail and element.tail.strip():
#         data['tail'] = element.tail.strip()
#     if element:
#         data['children'] = [element_to_dict(child) for child in element]
#     return data

# # Rest of your code...

# src_json = xmltodict.parse (xmlstr1)
# print("DEBUGGG")
# target_json=xmltodict.parse(xmlstr2)
# print(src_json)
# print (target_json)
# diff=DeepDiff(src_json,target_json)
# print("*"*100)
# print (diff)
# print(json.dumps(diff, default=serialize))

# data_str = json.dumps(diff, default=serialize)

# try:
#     # Try to load the string as JSON
#     data = json.loads(data_str)
# except json.JSONDecodeError:
#     # If it's not in JSON format, assume it's already a dictionary
#     data = eval(data_str)

# output = {}
# for key, value in data.items():
#     if key == 'dictionary_item_added':
#         tagname = value[0].split("'")[-2]
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = None
#         output['Except'] = None
#         output['test-result'] = 'fail'
#     else:
#         nested_key = list(value.keys())[0]  # Get the nested key
#         tagname = nested_key.split("'")[-2]  # Extract the tagname from the nested key
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = value[nested_key]['new_value']
#         output['Except'] = value[nested_key]['old_value']
#         output['test-result'] = 'fail'


# # print(output)
# # ###################################################################



# # import re

# # input_string = "root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']"

# # # Define a regular expression pattern to match and capture the desired substring
# # pattern = r"'MtchgCrit'\]\['([^']+)'\]\['([^']+)'\]\['([^']+)'\](.*)"

# # # Search for the pattern in the input string
# # match = re.search(pattern, input_string)

# # if match:
# #     groups = match.groups()
# #     output_string = "<" + "><".join(groups[:-1]) + ">"
# #     print(output_string)
# # else:
# #     print("Pattern not found")


# # {"dictionary_item_added": ["root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['CtrctMtchgCrit']['ISIN']"], "values_changed": {"root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']": {"new_value": "AAP", "old_value": "AAPA"}}}




# # if key == 'dictionary_item_added':

# # 	result = {tagname :'<CtrctMtchgCrit><ISIN>'
# # 	eod : null
# # 	Except : 
# # 	test-result : fail}
# # else:
# # 	result = {tagname :'<TxMtchgCrit><PltfmIdr><Val1>'
# # 	eod : AAP
# # 	Except : AAPA
# # 	test-result : fail}

##################################################################################################################################################################

import xml.etree.ElementTree as ET

# Input XML string
xml_data = """<BizData xmlns="urn:iso:std:iso:20022:tech:xsd:head.003.001.01"
    xmlns:xsi="http://yes.com"
    xmlns:n1="urn:iso:std:iso:20022:tech:xsd:head.001.001.02" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.003.001.01 head.003.001.02_DTCC.xsd">
    <Hdr>
        <AppHdr
            xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.02"
            xmlns:xsi="http://yes.com" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.001.001.02 head.001.001.02.xsd">
            <Fr>
                <OrgId>
                    <Id>
                        <OrgId>
                            <Othr>
                                <Id>DDRIE</Id>
                            </Othr>
                        </OrgId>
                    </Id>
                </OrgId>
            </Fr>
            <To>
                <OrgId>
                    <Id>
                        <OrgId>
                            <Othr>
                                <Id>2N07</Id>
                            </Othr>
                        </OrgId>
                    </Id>
                </OrgId>
            </To>
            <BizMsgIdr>Derivatives EOD Recon Report</BizMsgIdr>
            <MsgDefIdr>auth.091.001.02</MsgDefIdr>
            <CreDt>2024-04-13T08:48:24z</CreDt>
        </AppHdr>
    </Hdr>
    <Pyld>
    <Document
        xmlns="urn:iso:std:iso:20022:tech:xsd:head.091.001.02"
        xmlns:xsi="http://yes.com" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.091.001.02 auth.091.001.02_ESMAUG_DATREC_1.0.0.xsd">
        <DerivsTradRcncltnSttstclRpt>
            <RcnltnSttstcs>
                <Rpt>
                    <RefDT>2024-4-12</RefDT>
                    <RcnltnCtgrs>
                        <RptgRqrmnt>
                            <RptgTp>TWOS</RptgTp>
                            <Pairg>PARD</Pairg>
                            <Rcncltn>NREC</Rcncltn>
                            <ValtnRcncltn>NOAP</ValtnRcncltn>
                            <Rvvd>false</Rvvd>
                            <FrthrMod>true</FrthrMod>
                        </RptgRqrmnt>
                    </RcnltnCtgrs>
                    <Tt1NbOfTxs>323</Tt1NbOfTxs>
                    <TxDtls>
                        <CtrPtyId>
                            <RptgCtrPty>
                                <LEI>529900FDQEQ91XN3W228</LEI>
                            </RptgCtrPty>
                            <OthrCtrPty>
                                <Lg1>
                                    <LEI>549300681JNVQWG2CM14</LEI>
                                </Lg1>
                            </OthrCtrPty>
                            <RptSubmitgNtty>
                                <LEI>5493004VCP8BLKLM5895</LEI>
                            </RptSubmitgNtty>
                            <NttyRspnsblForRpt>
                                <LEI>52990069T419C3RYDL08</LEI>
                            </NttyRspnsblForRpt>
                        </CtrPtyId>
                        <Tt1NbOfTxs>156</Tt1NbOfTxs>
                        <RcncltnRpt>
                            <TxId>
                                <UnqIdr>
                                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                                </UnqIdr>
                            </TxId>
                            <MtchgCrit>
                                <CtrctMtchgCrit>
                                    <ISIN>
                                        <Val2>US9311421039</Val2>
                                    </ISIN>
                                    <UnqPdctIdr>
                                        <Val1>
                                            <Id>QZTF0Q7B08N4</Id>
                                        </Val1>
                                    </UnqPdctIdr>
                                </CtrctMtchgCrit>
                                <TxMtchgCrit>
                                    <PltfmIdr>
                                        <Val1>AAPA</Val1>
                                        <Val2>4AXE</Val2>
                                    </PltfmIdr>
                                </TxMtchgCrit>
                            </MtchgCrit>
                        </RcncltnRpt>

                        <RcncltnRpt>
                            <TxId>
                                <UnqIdr>
                                    <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
                                </UnqIdr>
                            </TxId>
                            <MtchgCrit>
                                <CtrctMtchgCrit>
                                    <CtrctTp>
                                        <Val1>FORW</Val1>
                                        <Val2>OTHR</Val2>
                                    </CtrctTp>
                                </CtrctMtchgCrit>
                            </MtchgCrit>
                        </RcncltnRpt>
                    </TxDtls>
                    <TxDtls>
                        <CtrPtyId>
                            <RptgCtrPty>
                                <LEI>529900FDQEQ91XN3W228</LEI>
                            </RptgCtrPty>
                            <OthrCtrPty>
                                <Lg1>
                                    <LEI>549300681JNVQWG2CM14</LEI>
                                </Lg1>
                            </OthrCtrPty>
                            <RptSubmitgNtty>
                                <LEI>5493004VCP8BLKLM5895</LEI>
                            </RptSubmitgNtty>
                            <NttyRspnsblForRpt>
                                <LEI>52990069T419C3RYDL08</LEI>
                            </NttyRspnsblForRpt>
                        </CtrPtyId>
                        <Tt1NbOfTxs>1466</Tt1NbOfTxs>
                        <RcncltnRpt>
                            <TxId>
                                <UnqIdr>
                                    <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
                                </UnqIdr>
                            </TxId>
                            <MtchgCrit>
                                <CtrctMtchgCrit>
                                    <ISIN>
                                        <Val2>US9311421039</Val2>
                                    </ISIN>
                                    <UnqPdctIdr>
                                        <Val1>
                                            <Id>QZTF0Q7B08N4</Id>
                                        </Val1>
                                    </UnqPdctIdr>
                                </CtrctMtchgCrit>
                                <TxMtchgCrit>
                                    <PltfmIdr>
                                        <Val1>AAPA</Val1>
                                        <Val2>4AXE</Val2>
                                    </PltfmIdr>
                                </TxMtchgCrit>
                            </MtchgCrit>
                        </RcncltnRpt>
                    </TxDtls>
                    <TxDtls>
                        <CtrPtyId>
                            <RptgCtrPty>
                                <LEI>529900FDQEQ91XN3W229</LEI>
                            </RptgCtrPty>
                            <OthrCtrPty>
                                <Lg1>
                                    <LEI>549300681JNVQWG2CM14</LEI>
                                </Lg1>
                            </OthrCtrPty>
                            <RptSubmitgNtty>
                                <LEI>5493004VCP8BLKLM5895</LEI>
                            </RptSubmitgNtty>
                            <NttyRspnsblForRpt>
                                <LEI>52990069T419C3RYDL08</LEI>
                            </NttyRspnsblForRpt>
                        </CtrPtyId>
                        <Tt1NbOfTxs>1466</Tt1NbOfTxs>
                        <RcncltnRpt>
                            <TxId>
                                <UnqIdr>
                                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                                </UnqIdr>
                            </TxId>
                            <MtchgCrit>
                                <CtrctMtchgCrit>
                                    <ISIN>
                                        <Val2>US9311421039</Val2>
                                    </ISIN>
                                    <UnqPdctIdr>
                                        <Val1>
                                            <Id>QZTF0Q7B08N4</Id>
                                        </Val1>
                                    </UnqPdctIdr>
                                </CtrctMtchgCrit>
                                <TxMtchgCrit>
                                    <PltfmIdr>
                                        <Val1>AAPA</Val1>
                                        <Val2>4AXE</Val2>
                                    </PltfmIdr>
                                </TxMtchgCrit>
                            </MtchgCrit>
                        </RcncltnRpt>
                    </TxDtls>
                </Rpt>
            </RcnltnSttstcs>
        </DerivsTradRcncltnSttstclRpt>
    </Document>
</Pyld>
</BizData>"""

# Namespace dictionary
namespaces = {
    'head003': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'head001': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'head091': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02'
}

# Parse XML
root = ET.fromstring(xml_data)

# Create an output element to store the result
output = ET.Element('TxDtls')

# Iterate through TxDtls and filter based on LEI
for tx_dtls in root.findall('.//head091:TxDtls', namespaces):
    lei = tx_dtls.find('.//head091:RptgCtrPty/head091:LEI', namespaces)
    if lei is not None and lei.text == '529900FDQEQ91XN3W228':
        for rcncltn_rpt in tx_dtls.findall('head091:RcncltnRpt', namespaces):
            output.append(rcncltn_rpt)

# Print the result as a string
output_str = ET.tostring(output, encoding='unicode')


output_str = output_str.replace('ns0:', '')
print(output_str)

##################################################################################################################################################################


# import pandas as pd

# # Read data from CSV file
# df = pd.read_csv('/Users/ranjithrreddyabbidi/ranjith/test.csv')

# # Print column names to verify them
# print(df.columns)

# # Assuming the column names are correct after verification
# distinct_df = df.drop_duplicates(subset=['Report Submitting entity ID', 'Entity responsible for reporting', 'Counterparty 1 (Reporting counterparty)'])

# # Convert the DataFrame to a list of dictionaries
# distinct_data = distinct_df.to_dict(orient='records')

##############################################################################################################################################################

# import xml.etree.ElementTree as ET

# # Read XML from file
# with open('/Users/ranjithrreddyabbidi/ranjith/final_input_xml.py', 'r') as file:
#     xml_data = file.read()

# # Namespace dictionary
# namespaces = {
#     'head003': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
#     'head001': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
#     'head091': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02'
# }

# # Parse XML
# root = ET.fromstring(xml_data)

# # Create an output element to store the result
# output = ET.Element('TxDtls')

# # Iterate through TxDtls and filter based on LEI
# for tx_dtls in root.findall('.//head091:TxDtls', namespaces):
#     lei = tx_dtls.find('.//head091:RptgCtrPty/head091:LEI', namespaces)
#     if lei is not None and lei.text == '529900FDQEQ91XN3W228':
#         for rcncltn_rpt in tx_dtls.findall('head091:RcncltnRpt', namespaces):
#             output.append(rcncltn_rpt)

# # Convert the output to a string
# output_str = ET.tostring(output, encoding='unicode')

# # Remove namespace prefixes from the result
# output_str = output_str.replace('ns0:', '')
# print(output_str)


import xml.etree.ElementTree as ET
import json

# Sample input JSON data
input_data = '''
[
    {
        "RptgCtrPty": "529900FDQEQ91XN3W228",
        "OthrCtrPty": "549300681JNVQWG2CM14"
    },
    {
        "RptgCtrPty": "1111111111111111",
        "OthrCtrPty": "222222222222222222"
    }
]
'''

# Read XML from file
with open('/Users/ranjithrreddyabbidi/ranjith/final_input_xml.py', 'r') as file:
    xml_data = file.read()

# Parse the input JSON data
criteria_list = json.loads(input_data)

# Namespace dictionary
namespaces = {
    'head003': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'head001': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'head091': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02'
}

# Parse XML
root = ET.fromstring(xml_data)

# Create an output element to store the result
output = ET.Element('TxDtls')

# Iterate through each set of criteria
for criteria in criteria_list:
    rptg_ctr_pty_lei = criteria.get("RptgCtrPty")
    othr_ctr_pty_lei = criteria.get("OthrCtrPty")
    
    # Iterate through TxDtls and filter based on LEI criteria
    for tx_dtls in root.findall('.//head091:TxDtls', namespaces):
        rptg_lei = tx_dtls.find('.//head091:RptgCtrPty/head091:LEI', namespaces)
        othr_lei = tx_dtls.find('.//head091:OthrCtrPty/head091:Lg1/head091:LEI', namespaces)
        
        if rptg_lei is not None and othr_lei is not None:
            if rptg_lei.text == rptg_ctr_pty_lei and othr_lei.text == othr_ctr_pty_lei:
                for rcncltn_rpt in tx_dtls.findall('head091:RcncltnRpt', namespaces):
                    output.append(rcncltn_rpt)

# Convert the output to a string
output_str = ET.tostring(output, encoding='unicode')

# Remove namespace prefixes from the result
output_str = output_str.replace('ns0:', '')
print(output_str)

with open('/Users/ranjithrreddyabbidi/ranjith/final_output_xml.py', 'w') as file:
    file.write(output_str)


# # Print the distinct data
# print(distinct_data)

