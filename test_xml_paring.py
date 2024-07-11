
import xml.etree.ElementTree as ET
import json
import os


input_data = '''
[
    {
        "RptgCtrPty": "529900FDQEQ91XN3W228",
        "OthrCtrPty": "549300681JNVQWG2CM14",
        "Paring": "PARD",
        "Rcncltn": "NREC",
        "Rvvd": "false"
    },
    {
        "RptgCtrPty": "1111111111111111",
        "OthrCtrPty": "222222222222222222",
        "Paring": "PARD0",
        "Rcncltn": "NREC",
        "Rvvd": "false"
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

for criteria in criteria_list:

    rptg_ctr_pty_lei = criteria.get("RptgCtrPty")
    othr_ctr_pty_lei = criteria.get("OthrCtrPty")
    Paring = criteria.get("Paring")
    Rcncltn = criteria.get("Rcncltn")
    Rvvd = criteria.get("Rvvd")

    rcnltn_ctgrs = ET.SubElement(output, 'RcnltnCtgrs')
    rptg_rqrmnt = ET.SubElement(rcnltn_ctgrs, 'RptgRqrmnt')
    ET.SubElement(rptg_rqrmnt, 'RptgTp').text = 'TWOS'
    ET.SubElement(rptg_rqrmnt, 'Pairg').text = Paring
    ET.SubElement(rptg_rqrmnt, 'Rcncltn').text = Rcncltn
    ET.SubElement(rptg_rqrmnt, 'ValtnRcncltn').text = 'NOAP'
    ET.SubElement(rptg_rqrmnt, 'Rvvd').text = Rvvd
    ET.SubElement(rptg_rqrmnt, 'FrthrMod').text = 'true'
    txdtl = ET.SubElement(output, 'Txdtl')
    ctr_pty_id = ET.SubElement(txdtl, 'CtrPtyId')
    
    
    # Add RptgCtrPty and OthrCtrPty elements
    rptg_ctr_pty = ET.SubElement(ctr_pty_id, 'RptgCtrPty')
    ET.SubElement(rptg_ctr_pty, 'LEI').text = rptg_ctr_pty_lei
    
    othr_ctr_pty = ET.SubElement(ctr_pty_id, 'OthrCtrPty')
    lg1 = ET.SubElement(othr_ctr_pty, 'Lg1')
    ET.SubElement(lg1, 'LEI').text = othr_ctr_pty_lei
    

    file_path = '/Users/ranjithrreddyabbidi/ranjith/final_input_xml.xml'
    print(file_path, "62"*10)
    file_tree = ET.parse(file_path)
    file_root = file_tree.getroot()

    path = '/Users/ranjithrreddyabbidi/ranjith/test_xml'
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        print(file_path, "62"*10)
        file_tree = ET.parse(file_path)
        file_root = file_tree.getroot()
    
        rptg_rqrmnt = file_root.find(f".//{{{namespaces['head091']}}}RptgRqrmnt")
        if rptg_rqrmnt is not None:
            paring_xml = rptg_rqrmnt.find(f".//{{{namespaces['head091']}}}Pairg")
            rcncltn_xml = rptg_rqrmnt.find(f".//{{{namespaces['head091']}}}Rcncltn")
            rvvd_xml = rptg_rqrmnt.find(f".//{{{namespaces['head091']}}}Rvvd")
            if paring_xml is not None and rcncltn_xml is not None and rvvd_xml is not None:
                
                print(paring_xml.text, Paring, "73"*10)
                print(rcncltn_xml.text, Rcncltn, "74"*10)
                print(rvvd_xml.text, Rvvd, "75"*10)
                if paring_xml.text == Paring and rcncltn_xml.text == Rcncltn and rvvd_xml.text == Rvvd:
                    with open(file_path, 'r') as file:
                        xml_data = file.read()

                    root = ET.fromstring(xml_data)

                    for tx_dtls in root.findall('.//head091:TxDtls', namespaces):
                        rptg_lei = tx_dtls.find('.//head091:RptgCtrPty/head091:LEI', namespaces)
                        othr_lei = tx_dtls.find('.//head091:OthrCtrPty/head091:Lg1/head091:LEI', namespaces)
                        
                        if rptg_lei is not None and othr_lei is not None:
                            if rptg_lei.text == rptg_ctr_pty_lei and othr_lei.text == othr_ctr_pty_lei:
                                for rcncltn_rpt in tx_dtls.findall('head091:RcncltnRpt', namespaces):
                                    txdtl.append(rcncltn_rpt)
                else:
                    continue
            else:
                continue
        else:
            continue

output_str = ET.tostring(output, encoding='unicode')

output_str = output_str.replace('ns0:', '')

print(output_str)

with open('/Users/ranjithrreddyabbidi/ranjith/final_output_xml_back.xml', 'w') as file:
    file.write(output_str)
