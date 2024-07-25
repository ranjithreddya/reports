import xml.etree.ElementTree as ET

# Sample XML input
xml_data = '''<RPT xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
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
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>529900FDQEQ91XN3W228</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>549300681JNVQWG2CM14</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
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
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>549300681JNVQWG2CM14</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>529900FDQEQ91XN3W228</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>11111111111111111111111111111111111111111Ranjith</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                <RptgCtrPty>
                    <LEI>549300681JNVQWG2CM14</LEI>
                </RptgCtrPty>
                <OthrCtrPty>
                    <Lg1>
                        <LEI>529900FDQEQ91XN3W228</LEI>
                    </Lg1>
                </OthrCtrPty>
                <RptSubmitgNtty>
                    <LEI>5493004VCP8BLKLM5895</LEI>
                </RptSubmitgNtty>
                <NttyRspnsblForRpt>
                    <LEI>52990069T419C3RYDL08</LEI>
                </NttyRspnsblForRpt>
            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
    <RcnltnCtgrs>
        <RptgRqrmnt>
            <RptgTp>TWOS</RptgTp>
            <Pairg>PARD0</Pairg>
            <Rcncltn>NREC</Rcncltn>
            <ValtnRcncltn>NOAP</ValtnRcncltn>
            <Rvvd>false</Rvvd>
            <FrthrMod>true</FrthrMod>
        </RptgRqrmnt>
    </RcnltnCtgrs>
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>1111111111111111</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>222222222222222222</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>11111111111111111111111111111111111111111</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
</RPT>'''

# Parse the XML
root = ET.fromstring(xml_data)

# Define the replacement function
def replace_unqtxidr(unqtxidr):
    if unqtxidr.startswith('NK') or unqtxidr.startswith('AK'):
        return unqtxidr[:2] + 'ranjith' + unqtxidr[14:]
    return unqtxidr

# Iterate through all UnqTxIdr elements and replace their values
for unqtxidr in root.findall('.//UnqTxIdr'):
    old_value = unqtxidr.text
    new_value = replace_unqtxidr(old_value)
    unqtxidr.text = new_value

# Output the modified XML
new_xml_data = ET.tostring(root, encoding='unicode')

print(new_xml_data)
