# Create a new XML structure
new_root = ET.Element("NewRoot")
new_tx_dtls = ET.SubElement(new_root, "NewTxDtls")

# Iterate over rows in the CSV file
for csv_dict in csv_reader:
    matching_data = None
    for elem in tx_dtls:
        rpt_submitg_ntty_element1 = elem.find('.//ns3:CtrPtyId/ns3:RptSubmitgNtty', namespaces=ns)
        if rpt_submitg_ntty_element1 is not None:
            lei_value = rpt_submitg_ntty_element1.text.strip() if rpt_submitg_ntty_element1.text else None

        if rpt_submitg_ntty_element1 is not None and lei_value == csv_dict["Report Submitting entity ID"]:
            matching_data = elem
            break

    if matching_data is not None:
        unq_tx_idr_element = matching_data.find('.//ns3:UnqTxIdr', namespaces=ns)
        if unq_tx_idr_element is not None and unq_tx_idr_element.text == "NK040824243049TC99999SEUREFIT51547XCOMNEGR93":
            rcncltn_rpt_element = matching_data.find('.//ns3:RcncltnRpt', namespaces=ns)
            if rcncltn_rpt_element is not None:
                # Append the RcncltnRpt block to the new XML structure
                new_tx_dtls.append(rcncltn_rpt_element)
        else:
            print("UnqTxIdr not found.")
    else:
        print("No matching data found in XML.")

# Create a new XML tree from the root element
new_tree = ET.ElementTree(new_root)

# Write the new XML tree to a file
new_xml_file = "/Users/ranjithrreddyabbidi/ranjith/new_sample.xml"
new_tree.write(new_xml_file, encoding="utf-8", xml_declaration=True)

print("New XML file created successfully.")


######################################################################################################

# Create a new XML structure
new_root = ET.Element('NewRoot')

# Iterate over rows in the CSV file
for csv_dict in csv_reader:
    matching_data = None
    for elem in tx_dtls:
        rpt_submitg_ntty_element1 = elem.find('.//ns3:CtrPtyId/ns3:RptSubmitgNtty', namespaces=ns)
        if rpt_submitg_ntty_element1 is not None:
            lei_value = rpt_submitg_ntty_element1.text
            lei_element = rpt_submitg_ntty_element1.find('.//ns3:LEI', namespaces=ns)
            lei_value = lei_element.text.strip() if lei_element is not None and lei_element.text else None

        if rpt_submitg_ntty_element1 is not None and lei_value == csv_dict["Report Submitting entity ID"]:
            matching_data = elem
            break

    if matching_data is not None:
        unq_tx_idr_element = matching_data.find('.//ns3:UnqTxIdr', namespaces=ns)
        if unq_tx_idr_element is not None and unq_tx_idr_element.text == "NK040824243049TC99999SEUREFIT51547XCOMNEGR93":
            rcncltn_rpt_element = matching_data.find('.//ns3:RcncltnRpt', namespaces=ns)
            if rcncltn_rpt_element is not None:
                # Append the RcncltnRpt block to the new XML structure
                new_root.append(rcncltn_rpt_element)
        else:
            print("UnqTxIdr not found.")
    else:
        print("No matching data found in XML.")

# Create a new XML tree with the updated structure
new_tree = ET.ElementTree(new_root)

# Write the new XML structure to a file
new_xml_file = "/Users/ranjithrreddyabbidi/ranjith/new_sample.xml"
new_tree.write(new_xml_file, encoding="utf-8", xml_declaration=True)
