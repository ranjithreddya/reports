import csv
import xml.etree.ElementTree as ET
from lxml import etree

# Define the namespace map
ns = {
    'ns1': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'ns2': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'ns3': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02',
}

mapping_1 = {
    "Report Submitting entity ID": "RptSubmitgNtty",
    "Entity responsible for reporting": "NttyRspnsblForRpt",
    "Counterparty 1 (Reporting counterparty)": "RptgCtrPty",
    "Counterparty 2": "OthrCtrPty",
}

mapping_2 = {
    "UTI": "UnqTxIdr",
}

# Load the XML file
xml_file = "/Users/ranjithrreddyabbidi/ranjith/sample.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Use the namespace prefixes in your XPath expression
tx_dtls = root.findall('.//ns3:TxDtls', namespaces=ns)

# Print the results
print(tx_dtls)

# CSV file path
csv_file_path = "/Users/ranjithrreddyabbidi/ranjith/test.csv"

# Read from CSV file
with open(csv_file_path, 'r') as file:
    # Use csv.DictReader to read from the file
    csv_reader = csv.DictReader(file)
    
    # print(csv_reader.fieldnames, "122"*100)
    # Iterate over rows in the CSV file
    for csv_dict in csv_reader:
    	# print(csv_dict["Report Submitting entity ID"], "124"*100)
    	# print(csv_dict["Entity responsible for reporting"], "125"*100)
    	# print(csv_dict["Counterparty 1 (Reporting counterparty)"], "126"*100)
    	# print(csv_dict["Counterparty 2"], "127"*100)

    	matching_data = None
    	for elem in tx_dtls:
    		# rpt_submitg_ntty_element = elem.find('.//' + mapping_1["Report Submitting entity ID"])
    		# print(rpt_submitg_ntty_element, "132"*100)

    		rpt_submitg_ntty_element1 = elem.find('.//ns3:CtrPtyId/ns3:RptSubmitgNtty', namespaces=ns)
    		# print("rpt_submitg_ntty_element1:", rpt_submitg_ntty_element1, "*"*100)

    		if rpt_submitg_ntty_element1 is not None:
    			lei_value = rpt_submitg_ntty_element1.text
    			lei_element = rpt_submitg_ntty_element1.find('.//ns3:LEI', namespaces=ns)
    			lei_value = lei_element.text.strip() if lei_element.text else None
    			# print("LEI Value:", lei_value, "#"*100)

    		if rpt_submitg_ntty_element1 is not None and lei_value == csv_dict["Report Submitting entity ID"]:
    			matching_data = elem
    			break
    	print(matching_data, "130"*100)

    	if matching_data is not None:
            unq_tx_idr_element = elem.find('.//ns3:UnqTxIdr', namespaces=ns)
            if unq_tx_idr_element is not None and unq_tx_idr_element.text == "NK040824243049TC99999SEUREFIT51547XCOMNEGR93":
                rcncltn_rpt_element = elem.find('.//ns3:RcncltnRpt', namespaces=ns)
                # Print the complete RcncltnRpt block
                # print(ET.tostring(rcncltn_rpt_element, encoding='unicode'))

                # xml_string = ET.tostring(rcncltn_rpt_element, encoding='unicode', method='xml', short_empty_elements=False)
                # xml_string = xml_string.replace('ns0:', '')  # Remove the namespace prefix
                # print(xml_string)

                rcncltn_rpt_element.attrib.pop('{urn:iso:std:iso:20022:tech:xsd:head.091.001.02}xmlns', None)
                # Print the complete RcncltnRpt block
                xml_string = ET.tostring(rcncltn_rpt_element, encoding='unicode', method='xml', short_empty_elements=False)
                xml_string = xml_string.replace('ns0:', '') 
                print(xml_string)
            else:
                print("UnqTxIdr not found.")
    	else:
    		print("No matching data found in XML.")
