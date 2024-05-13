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
