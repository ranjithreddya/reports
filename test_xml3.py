import csv
import xml.etree.ElementTree as ET

# Define the namespace map
ns = {
    'ns1': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
    'ns2': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.02',
    'ns3': 'urn:iso:std:iso:20022:tech:xsd:head.091.001.02',
}

# Load the XML file
xml_file = "/Users/ranjithrreddyabbidi/ranjith/sample.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# CSV file path
csv_file_path = "/Users/ranjithrreddyabbidi/ranjith/test.csv"

# Create a new XML structure to hold matched data
result_root = ET.Element('TxDtls')

with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    for csv_dict in csv_reader:
        matching_data = None
        for tx_dtls in root.findall('.//ns3:TxDtls', namespaces=ns):
            rpt_submitg_ntty_element1 = tx_dtls.find('.//ns3:RptSubmitgNtty/ns3:LEI', namespaces=ns)
            if rpt_submitg_ntty_element1 is not None and rpt_submitg_ntty_element1.text.strip() == csv_dict["Report Submitting entity ID"]:
                matching_data = tx_dtls
                break

        if matching_data is not None:
            tx_id_elements = matching_data.findall('.//ns3:TxId', namespaces=ns)
            for tx_id_element in tx_id_elements:
                unq_tx_idr_element = tx_id_element.find('.//ns3:UnqIdr/ns3:UnqTxIdr', namespaces=ns)
                if unq_tx_idr_element is not None:
                    # Compare the UTI with the value from the CSV
                    uti = csv_dict["UTI"]
                    if unq_tx_idr_element.text.strip() == uti:
                        # Append the children of the matching_data to result_root
                        for child in matching_data:
                            result_root.append(child)
                        break
            else:
                print("UTI not found.")
        else:
            print("No matching data found in XML.")

# Write the result to an XML file
result_tree = ET.ElementTree(result_root)
result_tree.write("/Users/ranjithrreddyabbidi/ranjith/matched_data.xml", encoding='utf-8', xml_declaration=True)

