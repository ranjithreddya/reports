import xml.etree.ElementTree as ET

# Parse the XML from a file
tree = ET.parse('your_file.xml')
root = tree.getroot()

# Extract UnqTxIdr values and construct the dictionary
output_dict = {}
for i, rcncltn_rpt in enumerate(root.findall('.//RcncltnRpt')):
    unq_tx_idr = rcncltn_rpt.find('.//UnqTxIdr').text
    output_dict[str(i)] = unq_tx_idr

print(output_dict)



# import xml.etree.ElementTree as ET

# # Parse the XML input
# xml_string = '''
# <TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
#     <RcncltnRpt>
#         <TxId>
#             <UnqIdr>
#                 <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR95</UnqTxIdr>
#             </UnqIdr>
#         </TxId>
#         <MtchgCrit>
#             <CtrctMtchgCrit>
#                 <ISIN>
#                     <Val2>US9311421039</Val2>
#                 </ISIN>
#                 <UnqPdctIdr>
#                     <Val1>
#                         <Id>QZTF0Q7B08N4</Id>
#                     </Val1>
#                 </UnqPdctIdr>
#             </CtrctMtchgCrit>
#             <TxMtchgCrit>
#                 <PltfmIdr>
#                     <Val1>AAPA</Val1>
#                     <Val2>4AXE</Val2>
#                 </PltfmIdr>
#             </TxMtchgCrit>
#         </MtchgCrit>
#     </RcncltnRpt>
#     <RcncltnRpt>
#         <TxId>
#             <UnqIdr>
#                 <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
#             </UnqIdr>
#         </TxId>
#         <MtchgCrit>
#             <CtrctMtchgCrit>
#                 <ISIN>
#                     <Val2>US9311421039</Val2>
#                 </ISIN>
#                 <UnqPdctIdr>
#                     <Val1>
#                         <Id>QZTF0Q7B08N4</Id>
#                     </Val1>
#                 </UnqPdctIdr>
#             </CtrctMtchgCrit>
#             <TxMtchgCrit>
#                 <PltfmIdr>
#                     <Val1>AAPA</Val1>
#                     <Val2>4AXE</Val2>
#                 </PltfmIdr>
#             </TxMtchgCrit>
#         </MtchgCrit>
#     </RcncltnRpt>
# </TxDtls>
# '''

# root = ET.fromstring(xml_string)

# # Extract UnqTxIdr values and construct the dictionary
# output_dict = {}
# for i, rcncltn_rpt in enumerate(root.findall('.//RcncltnRpt')):
#     unq_tx_idr = rcncltn_rpt.find('.//UnqTxIdr').text
#     output_dict[str(i)] = unq_tx_idr
