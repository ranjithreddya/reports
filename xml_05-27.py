import xml.etree.ElementTree as ET
import json

# Sample input JSON data for criteria and UTIs
criteria_data = '''
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

uti_data = '''
[
    "NK040824243049TC99999SEUREFIT51547XCOMNEGR93",
    "NK040824243049TC99999SEUREFIT516115XCOMNEGR964",
    "NK0408242430490000000000000000000000000",
    "11111111111111111111111111111111111111111"
]
'''

# Read XML from file
with open('/Users/ranjithrreddyabbidi/ranjith/final_input_xml.xml', 'r') as file:
    xml_data = file.read()

# Parse the input JSON data
criteria_list = json.loads(criteria_data)
uti_list = json.loads(uti_data)

# Namespace dictionary
namespaces = {
    '': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'n1': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'n2': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02'
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
    for tx_dtls in root.findall('.//n2:TxDtls', namespaces):
        rptg_lei = tx_dtls.find('.//n2:RptgCtrPty/n2:LEI', namespaces)
        othr_lei = tx_dtls.find('.//n2:OthrCtrPty/n2:Lg1/n2:LEI', namespaces)

        if rptg_lei is not None and othr_lei is not None:
            if rptg_lei.text == rptg_ctr_pty_lei and othr_lei.text == othr_ctr_pty_lei:
                for rcncltn_rpt in tx_dtls.findall('n2:RcncltnRpt', namespaces):
                    unq_tx_idr = rcncltn_rpt.find('.//n2:UnqTxIdr', namespaces)
                    if unq_tx_idr is not None and unq_tx_idr.text in uti_list:
                        output.append(rcncltn_rpt)

# Convert the output to a string
output_str = ET.tostring(output, encoding='unicode')

# Remove namespace prefixes from the result
output_str = output_str.replace('n2:', '')
output_str = output_str.replace('xmlns="urn:iso:std:iso:20022:tech:xsd:head.091.001.02"', '')

# Print the output
print(output_str)

# Write the output to a file
with open('/Users/ranjithrreddyabbidi/ranjith/final_output_xml.xml', 'w') as file:
    file.write(output_str)





# <BizData xmlns="urn:iso:std:iso:20022:tech:xsd:head.003.001.01"
#     xmlns:xsi="http://yes.com"
#     xmlns:n1="urn:iso:std:iso:20022:tech:xsd:head.001.001.02" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.003.001.01 head.003.001.02_DTCC.xsd">
#     <Hdr>
#         <AppHdr
#             xmlns="urn:iso:std:iso:20022:tech:xsd:head.001.001.02"
#             xmlns:xsi="http://yes.com" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.001.001.02 head.001.001.02.xsd">
#             <Fr>
#                 <OrgId>
#                     <Id>
#                         <OrgId>
#                             <Othr>
#                                 <Id>DDRIE</Id>
#                             </Othr>
#                         </OrgId>
#                     </Id>
#                 </OrgId>
#             </Fr>
#             <To>
#                 <OrgId>
#                     <Id>
#                         <OrgId>
#                             <Othr>
#                                 <Id>2N07</Id>
#                             </Othr>
#                         </OrgId>
#                     </Id>
#                 </OrgId>
#             </To>
#             <BizMsgIdr>Derivatives EOD Recon Report</BizMsgIdr>
#             <MsgDefIdr>auth.091.001.02</MsgDefIdr>
#             <CreDt>2024-04-13T08:48:24z</CreDt>
#         </AppHdr>
#     </Hdr>
#     <Pyld>
#     <Document
#         xmlns="urn:iso:std:iso:20022:tech:xsd:head.091.001.02"
#         xmlns:xsi="http://yes.com" xsi:schemaLocation="urn:iso:std:iso:20022:tech:xsd:head.091.001.02 auth.091.001.02_ESMAUG_DATREC_1.0.0.xsd">
#         <DerivsTradRcncltnSttstclRpt>
#             <RcnltnSttstcs>
#                 <Rpt>
#                     <RefDT>2024-4-12</RefDT>
#                     <RcnltnCtgrs>
#                         <RptgRqrmnt>
#                             <RptgTp>TWOS</RptgTp>
#                             <Pairg>PARD</Pairg>
#                             <Rcncltn>NREC</Rcncltn>
#                             <ValtnRcncltn>NOAP</ValtnRcncltn>
#                             <Rvvd>false</Rvvd>
#                             <FrthrMod>true</FrthrMod>
#                         </RptgRqrmnt>
#                     </RcnltnCtgrs>
#                     <Tt1NbOfTxs>323</Tt1NbOfTxs>
#                     <TxDtls>
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
#                             </MtchgCrit>
#                         </RcncltnRpt>

#                         <RcncltnRpt>
#                             <TxId>
#                                 <UnqIdr>
#                                     <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
#                                 </UnqIdr>
#                             </TxId>
#                             <MtchgCrit>
#                             </MtchgCrit>
#                         </RcncltnRpt>
#                     </TxDtls>
#                     <TxDtls>
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
#                         <Tt1NbOfTxs>1466</Tt1NbOfTxs>
#                         <RcncltnRpt>
#                             <TxId>
#                                 <UnqIdr>
#                                     <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
#                                 </UnqIdr>
#                             </TxId>
#                             <MtchgCrit>
#                             </MtchgCrit>
#                         </RcncltnRpt>
#                     </TxDtls>
#                     <TxDtls>
#                         <CtrPtyId>
#                             <RptgCtrPty>
#                                 <LEI>1111111111111111</LEI>
#                             </RptgCtrPty>
#                             <OthrCtrPty>
#                                 <Lg1>
#                                     <LEI>222222222222222222</LEI>
#                                 </Lg1>
#                             </OthrCtrPty>
#                             <RptSubmitgNtty>
#                                 <LEI>5493004VCP8BLKLM5895</LEI>
#                             </RptSubmitgNtty>
#                             <NttyRspnsblForRpt>
#                                 <LEI>52990069T419C3RYDL08</LEI>
#                             </NttyRspnsblForRpt>
#                         </CtrPtyId>
#                         <Tt1NbOfTxs>1466</Tt1NbOfTxs>
#                         <RcncltnRpt>
#                             <TxId>
#                                 <UnqIdr>
#                                     <UnqTxIdr>11111111111111111111111111111111111111111</UnqTxIdr>
#                                 </UnqIdr>
#                             </TxId>
#                             <MtchgCrit>
#                                 <CtrctMtchgCrit>
#                                 </CtrctMtchgCrit>
#                                 <TxMtchgCrit>
#                                 </TxMtchgCrit>
#                             </MtchgCrit>
#                         </RcncltnRpt>
#                     </TxDtls>
#                 </Rpt>
#             </RcnltnSttstcs>
#         </DerivsTradRcncltnSttstclRpt>
#     </Document>
# </Pyld>
# </BizData>
