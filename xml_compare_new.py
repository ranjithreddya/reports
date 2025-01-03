import xmltodict
import pandas as pd


def find_key(data, target_key):
    """
    Recursively searches for the target_key in a nested dictionary and returns the value.
    If the key is not found, returns None.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                # Recur for nested dictionary or list
                result = find_key(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, sub_item in enumerate(v):
                items.extend(flatten_dict(sub_item, f'{new_key}{sep}{i}', sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Function to handle multiple rows from different tags (like RPT, RPT2, TxId)
def flatten_xml_to_rows(xml_data):
    rows = []
    
    # Extract the root element (e.g., RcncltnRpt)
    scify_data = xml_data.get('scify', {}).get('test', {}).get('RcncltnRpt', {})
    
    # Iterate over each key in RcncltnRpt and handle nested lists like RPT, TxId
    # for tag, value in scify_data.items():
    for tag, value in xml_data.items():
        if isinstance(value, list):
            for item in value:
                # Flatten each item in the list (e.g., each RPT or TxId entry)
                flattened_row = flatten_dict(item, parent_key=f'RcncltnRpt_{tag}')
                rows.append(flattened_row)
        else:
            # If it's not a list, it's a single element (handle it as a single row)
            flattened_row = flatten_dict(value, parent_key=f'RcncltnRpt_{tag}')
            rows.append(flattened_row)

    return rows

# # Parse the XML data
# xml_data = '''
# <scify>
#     <test>
#         <RcncltnRpt>
#             <RPT>
#                 <abc>123a</abc>
#                 <dca>456a</dca>
#             </RPT>
#             <RPT>
#                 <abc>123a</abc>
#                 <dca>456a</dca>
#             </RPT>

#             <RPT2>
#                 <abc>123a</abc>
#                 <dca>456a</dca>
#             </RPT2>
#             <RPT2>
#                 <abc>123a</abc>
#                 <dca>456a</dca>
#             </RPT2>

#             <TxId>
#                 <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
#                 <CtrctMtchgCrit>
#                     <ISIN>
#                         <Val2>US9311421039</Val2>
#                     </ISIN>
#                     <UnqPdctIdr>
#                         <Val1>
#                             <Id>QZTF0Q7B08N4</Id>
#                         </Val1>
#                     </UnqPdctIdr>
#                 </CtrctMtchgCrit>
#                 <TxMtchgCrit>
#                     <PltfmIdr>
#                         <Val1>AAPA</Val1>
#                         <Val2>4AXE</Val2>
#                     </PltfmIdr>
#                 </TxMtchgCrit>
#             </TxId>
#             <TxId>
#                 <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
#                 <CtrctMtchgCrit>
#                     <UnqPdctIdr>
#                         <Val1>
#                             <Id>QZTF0Q7B08N4</Id>
#                         </Val1>
#                     </UnqPdctIdr>
#                 </CtrctMtchgCrit>
#                 <TxMtchgCrit>
#                     <PltfmIdr>
#                         <Val1>AAPA</Val1>
#                         <Val2>4AXE</Val2>
#                     </PltfmIdr>
#                 </TxMtchgCrit>
#             </TxId>
#         </RcncltnRpt>
#     </test>
# </scify>
# '''


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

# Parse the XML into a dictionary
xml_dict = xmltodict.parse(xml_data)

rcncltn_rpt = find_key(xml_dict, 'RcncltnRpt')  # need to update for loop

# Flatten the XML data
flattened_data = flatten_xml_to_rows(rcncltn_rpt)

# Convert to DataFrame (this will give you multiple rows, each corresponding to one tag like RPT, RPT2, or TxId)
df = pd.DataFrame(flattened_data)

# Save the DataFrame to CSV
df.to_csv('output19.csv', index=False)

# Show the DataFrame to verify
print(df)
