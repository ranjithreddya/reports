# import xml.etree.ElementTree as ET
# import csv

# # Load the XML file
# xml_file = "/Users/ranjithrreddyabbidi/ranjith/sample.xml"
# tree = ET.parse(xml_file)
# root = tree.getroot()

# # Define a function to remove namespace prefixes
# def remove_namespace_prefix(elem):
#     elem.tag = elem.tag.split('}')[-1]
#     for child in elem.iter():
#         child.tag = child.tag.split('}')[-1]

# # Remove namespace prefixes from the root and its descendants
# remove_namespace_prefix(root)

# # CSV file path
# csv_file_path = "/Users/ranjithrreddyabbidi/ranjith/test.csv"

# # Initialize an empty list to store results
# result = []

# for csv_dict in csv.DictReader(open(csv_file_path)):
#     for elem in root.findall('.//TxDtls'):
#         rpt_submitg_ntty_element1 = elem.find('.//CtrPtyId/RptSubmitgNtty')
#         if rpt_submitg_ntty_element1 is not None:
#             lei_value = rpt_submitg_ntty_element1.find('.//LEI').text.strip()
#             if lei_value == csv_dict["Report Submitting entity ID"]:
#                 result.append(elem)
#                 break

# # Create a new XML tree for the matching data
# matching_data_root = ET.Element("MatchingData")

# for elem in result:
#     matching_data_root.append(elem)

# # Create a new XML tree
# matching_data_tree = ET.ElementTree(matching_data_root)

# # Write the new XML tree to a file
# output_xml_file = "/Users/ranjithrreddyabbidi/ranjith/matching_data.xml"
# matching_data_tree.write(output_xml_file)

# print("Matching data has been written to", output_xml_file)


# output:
# <MatchingData><TxDtls>
#                         <CtrPtyId>
#                             <RptgCtrPty>
#                                 <LEI>529900FDQEQ91XN3W228</LEI>
#                             </RptgCtrPty>
#                             <OthrCtrPty>
#                                 <Lg1>
#                                     <LEI>549300681JNVQWG2CM14</LEI>
#                                 </Lg1>
#                             </OthrCtrPty>
#                             <RptSubmitgNtty>
#                                 <LEI>5493004VCP8BLKLM5895</LEI>
#                             </RptSubmitgNtty>
#                             <NttyRspnsblForRpt>
#                                 <LEI>52990069T419C3RYDL08</LEI>
#                             </NttyRspnsblForRpt>
#                         </CtrPtyId>
#                         <Tt1NbOfTxs>156</Tt1NbOfTxs>
#                         <RcncltnRpt>
#                             <TxId>
#                                 <UnqIdr>
#                                     <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
#                                 </UnqIdr>
#                             </TxId>
#                             <MtchgCrit>
#                                 <CtrctMtchg


# i only want <TxDtls>

import xml.etree.ElementTree as ET

# XML data
xml_data = '''
<TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
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
'''

# Parse XML
root = ET.fromstring(xml_data)

# Define the target UnqTxIdr
target_unq_tx_idr = "NK040824243049TC99999SEUREFIT51547XCOMNEGR93"

# Find the matching UnqTxIdr and print its child tag data
for rcncltn_rpt in root.findall('.//RcncltnRpt'):
    unq_tx_idr = rcncltn_rpt.find('.//UnqTxIdr').text
    if unq_tx_idr == target_unq_tx_idr:
        
        print("Found matching UnqTxIdr:", unq_tx_idr)
        for child in rcncltn_rpt:
            print("Child tag:", child.tag)
            print("Child text:", child.text)
