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
