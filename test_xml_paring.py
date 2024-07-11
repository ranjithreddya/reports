
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

criteria_list = json.loads(input_data)

# Namespace dictionary
namespaces = {
    'head003': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'head001': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'head091': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02'
}

file_path = '/Users/ranjithrreddyabbidi/ranjith/final_input_xml.xml'

output = ET.Element('RPT')

# Create RcnltnCtgrs and RptgRqrmnt elements


# Iterate through each set of criteria
for criteria in criteria_list:
    rcnltn_ctgrs = ET.SubElement(output, 'RcnltnCtgrs')
    rptg_rqrmnt = ET.SubElement(rcnltn_ctgrs, 'RptgRqrmnt')
    ET.SubElement(rptg_rqrmnt, 'RptgTp').text = 'TWOS'
    ET.SubElement(rptg_rqrmnt, 'Pairg').text = 'PARD'
    ET.SubElement(rptg_rqrmnt, 'Rcncltn').text = 'NREC'
    ET.SubElement(rptg_rqrmnt, 'ValtnRcncltn').text = 'NOAP'
    ET.SubElement(rptg_rqrmnt, 'Rvvd').text = 'false'
    ET.SubElement(rptg_rqrmnt, 'FrthrMod').text = 'true'
    txdtl = ET.SubElement(output, 'Txdtl')
    ctr_pty_id = ET.SubElement(txdtl, 'CtrPtyId')
    
    rptg_ctr_pty_lei = criteria.get("RptgCtrPty")
    othr_ctr_pty_lei = criteria.get("OthrCtrPty")
    
    # Add RptgCtrPty and OthrCtrPty elements
    rptg_ctr_pty = ET.SubElement(ctr_pty_id, 'RptgCtrPty')
    ET.SubElement(rptg_ctr_pty, 'LEI').text = rptg_ctr_pty_lei
    
    othr_ctr_pty = ET.SubElement(ctr_pty_id, 'OthrCtrPty')
    lg1 = ET.SubElement(othr_ctr_pty, 'Lg1')
    ET.SubElement(lg1, 'LEI').text = othr_ctr_pty_lei
    
    # Read XML data from file
    with open(file_path, 'r') as file:
        xml_data = file.read()

    root = ET.fromstring(xml_data)
    
    # Iterate through TxDtls and filter based on LEI criteria
    for tx_dtls in root.findall('.//head091:TxDtls', namespaces):
        rptg_lei = tx_dtls.find('.//head091:RptgCtrPty/head091:LEI', namespaces)
        othr_lei = tx_dtls.find('.//head091:OthrCtrPty/head091:Lg1/head091:LEI', namespaces)
        
        if rptg_lei is not None and othr_lei is not None:
            if rptg_lei.text == rptg_ctr_pty_lei and othr_lei.text == othr_ctr_pty_lei:
                for rcncltn_rpt in tx_dtls.findall('head091:RcncltnRpt', namespaces):
                    txdtl.append(rcncltn_rpt)

# Convert the output to a string
output_str = ET.tostring(output, encoding='unicode')

# Remove namespace prefixes from the result
output_str = output_str.replace('ns0:', '')

print(output_str)

# Write the output to a file
with open('/Users/ranjithrreddyabbidi/ranjith/final_output_xml_back.xml', 'w') as file:
    file.write(output_str)
