import xml.etree.ElementTree as ET
import csv

# Sample XML data (replace this with your XML content)
xml_data = '''
<RPT>
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
                <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
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
</RPT>
'''

# Parse the XML data
root = ET.fromstring(xml_data)

# Function to extract the tag path and value
def extract_values(element, path=""):
    if len(element) == 0:  # If the element has no children, it's a leaf node
        return {path: element.text}
    values = {}
    for child in element:
        new_path = f"{path}_{child.tag}" if path else child.tag
        values.update(extract_values(child, new_path))
    return values

# Prepare to collect all rows
rows = []

# Loop through all <RcncltnRpt> elements
for rcncltn_rpt in root.findall('RcncltnRpt'):
    row = extract_values(rcncltn_rpt)
    rows.append(row)

# Get the headers (column names) from the first row (keys of the dictionary)
headers = rows[0].keys()

# Write to CSV
with open('output.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print("CSV file 'output.csv' created successfully.")

###########################################################################################


import pandas as pd
import xmltodict

# Sample XML data (replace this with your XML content)
xml_data = '''
<RPT>
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
                <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
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
</RPT>
'''

# Parse XML into a dictionary using xmltodict
xml_dict = xmltodict.parse(xml_data)

# Normalize the data to flatten the nested structure
df = pd.json_normalize(xml_dict['RPT']['RcncltnRpt'], sep='_')

# Save the DataFrame to CSV
df.to_csv('output.csv', index=False)

print("CSV file 'output.csv' created successfully.")

###########################################################################



import pandas as pd
import xmltodict

xml_data = '''
    <RcncltnRpt>
        <TxId>
            <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
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
        </TxId>
        <TxId>
            <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
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
        </TxId>
    </RcncltnRpt>
    '''

xml_dict = xmltodict.parse(xml_data)

# # Normalize the data to flatten the nested structure
# df = pd.json_normalize(xml_dict['RcncltnRpt']['TxId'], sep='_')

# # Save the DataFrame to CSV
# df.to_csv('output5.csv', index=False)

# print("CSV file 'output5.csv' created successfully.")





# # Parse the XML data into a Python dictionary
# xml_dict = xmltodict.parse(xml_data)

# # Function to recursively flatten the dictionary and create paths for nested keys
# def flatten_dict(d, parent_key='', sep='_'):
#     items = []
#     for k, v in d.items():
#         new_key = f'{parent_key}{sep}{k}' if parent_key else k
#         if isinstance(v, dict):
#             items.extend(flatten_dict(v, new_key, sep=sep).items())  # Recursively flatten dictionaries
#         elif isinstance(v, list):
#             for i, sub_item in enumerate(v):
#                 items.extend(flatten_dict(sub_item, f'{new_key}{sep}{i}', sep=sep).items())  # Flatten lists
#         else:
#             items.append((new_key, v))  # Base case for primitive values
#     return dict(items)

# # Extract the 'TxId' entries (this could vary depending on the XML structure)
# tx_ids = xml_dict['RcncltnRpt']['TxId']

# # Flatten each TxId entry
# flattened_data = []

# for tx_id in tx_ids:
#     flattened_data.append(flatten_dict(tx_id, parent_key='RcncltnRpt_TxId'))

# # Convert the flattened data to a DataFrame
# df = pd.DataFrame(flattened_data)

# # Save the DataFrame to CSV
# df.to_csv('output9.csv', index=False)

# print("CSV file 'output9.csv' created successfully.")



##########################


# # Recursive function to flatten the XML data
# def flatten_dict(d, parent_key='', sep='_'):
#     items = []
#     for k, v in d.items():
#         new_key = f'{parent_key}{sep}{k}' if parent_key else k
#         if isinstance(v, dict):
#             items.extend(flatten_dict(v, new_key, sep=sep).items())  # Recursively flatten dicts
#         elif isinstance(v, list):
#             for i, sub_item in enumerate(v):
#                 items.extend(flatten_dict(sub_item, f'{new_key}{sep}{i}', sep=sep).items())  # Flatten lists
#         else:
#             items.append((new_key, v))  # Base case for primitive values
#     return dict(items)

# # Start with the root element and recursively flatten the XML structure
# flattened_data = flatten_dict(xml_dict)

# # Convert the flattened data to a DataFrame (if it's a list of dictionaries, we convert to DataFrame)
# df = pd.DataFrame([flattened_data])

# # Save the DataFrame to CSV
# df.to_csv('output10.csv', index=False)

# print("CSV file 'output10.csv' created successfully.")

##########################################
# # Function to recursively flatten the XML data
# def flatten_dict(d, parent_key='', sep='_'):
#     items = []
#     for k, v in d.items():
#         new_key = f'{parent_key}{sep}{k}' if parent_key else k
#         if isinstance(v, dict):
#             items.extend(flatten_dict(v, new_key, sep=sep).items())  # Recursively flatten dicts
#         elif isinstance(v, list):
#             for i, sub_item in enumerate(v):
#                 items.extend(flatten_dict(sub_item, f'{new_key}{sep}{i}', sep=sep).items())  # Flatten lists
#         else:
#             items.append((new_key, v))  # Base case for primitive values
#     return dict(items)

# # Extract the 'RcncltnRpt' entry and flatten it
# rcncltn_data = xml_dict['RcncltnRpt']

# # Now, we need to handle the case where 'TxId' is a list of multiple items
# flattened_data = []

# if isinstance(rcncltn_data['TxId'], list):
#     # If TxId is a list, we need to flatten each item and treat each as a separate row
#     for tx_id in rcncltn_data['TxId']:
#         flattened_data.append(flatten_dict(tx_id, parent_key='RcncltnRpt_TxId'))
# else:
#     # If there is only one TxId (not a list), we can flatten it directly
#     flattened_data.append(flatten_dict(rcncltn_data['TxId'], parent_key='RcncltnRpt_TxId'))

# # Convert the flattened data to a DataFrame
# df = pd.DataFrame(flattened_data)

# # Save the DataFrame to CSV
# df.to_csv('output12.csv', index=False)

# print("CSV file 'output12.csv' created successfully.")


# Parse the XML data into a Python dictionary
xml_dict = xmltodict.parse(xml_data)

# Recursive function to flatten the XML structure dynamically
def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            # Flatten nested dictionaries
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # For lists, iterate through and flatten each item separately
            for i, sub_item in enumerate(v):
                items.extend(flatten_dict(sub_item, f'{new_key}{sep}{i}', sep=sep).items())
        else:
            # Base case: append the value
            items.append((new_key, v))
    return dict(items)

# Function to handle multiple rows from lists (like TxId entries)
def flatten_xml_to_rows(xml_data):
    rows = []
    
    # Extract the root element (RcncltnRpt in this case)
    root = xml_data.get('RcncltnRpt', {})

    # Check if any key has a list (e.g., multiple TxId entries)
    for key, value in root.items():
        if isinstance(value, list):
            for item in value:
                # For each list item, flatten it and add as a new row
                rows.append(flatten_dict(item, parent_key=key))
        elif isinstance(value, dict):
            rows.append(flatten_dict(value, parent_key=key))

    return rows

# Extract and flatten all entries (assuming 'RcncltnRpt' contains lists and dicts)
flattened_data = flatten_xml_to_rows(xml_dict)

# Convert to DataFrame (this will give you multiple rows, each corresponding to one `TxId`)
df = pd.DataFrame(flattened_data)

# Save the DataFrame to CSV
df.to_csv('output13.csv', index=False)

print("CSV file 'output13.csv' created successfully.")
