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








##############################################################################################
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
    for tag, value in xml_data.items():
        if isinstance(value, list):
            for item in value:
                # Flatten each item in the list (e.g., each RPT or TxId entry)
                flattened_row = flatten_dict(item, parent_key=f'{tag}')
                rows.append(flattened_row)
        else:
            # If it's not a list, it's a single element (handle it as a single row)
            flattened_row = flatten_dict(value, parent_key=f'{tag}')
            rows.append(flattened_row)

    return rows

# Example function to process the table of XML data
def process_table_with_xml(df):
    # Create a list to store the new rows with additional columns from XML
    all_rows = []

    for index, row in df.iterrows():
        # Parse XML data from the current row (it assumes the XML data is in the 'xml_data' column)
        xml_data_str = row['xml_data']
        
        # Parse XML string into a dictionary
        xml_dict = xmltodict.parse(xml_data_str)
        
        # Extract the RcncltnRpt data from the parsed XML
        rcncltn_rpt = find_key(xml_dict, 'RcncltnRpt')

        # Flatten the XML data into rows
        flattened_data = flatten_xml_to_rows(rcncltn_rpt)

        # For each flattened row, combine with the original row (col1, col2)
        for data_row in flattened_data:
            combined_row = {**row.to_dict(), **data_row}
            all_rows.append(combined_row)

    # Convert the processed rows into a DataFrame
    processed_df = pd.DataFrame(all_rows)

    return processed_df

# Sample input table with XML data
data = {
    'col1': ['abc', 'def'],
    'col2': [123, 456],
    'xml_data': [
        '''<RcncltnRpt>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>NK040824243049TC88888SEUREFIT51547XCOMNEGR94</UnqTxIdr>
                <CtrctMtchgCrit>
                    <ISIN>
                        <Val2>US1234567890</Val2>
                    </ISIN>
                    <UnqPdctIdr>
                        <Val1>
                            <Id>ABCD1234</Id>
                        </Val1>
                    </UnqPdctIdr>
                </CtrctMtchgCrit>
                <TxMtchgCrit>
                    <PltfmIdr>
                        <Val1>XYZ</Val1>
                        <Val2>5BXY</Val2>
                    </PltfmIdr>
                </TxMtchgCrit>
            </TxId>
        </RcncltnRpt>'''
    ]
}

df = pd.DataFrame(data)

# Process the table and extract XML data into new columns
processed_df = process_table_with_xml(df)

# Save the resulting DataFrame to CSV
processed_df.to_csv('output_with_xml.csv', index=False)

# Show the resulting DataFrame to verify
print(processed_df)




import csv
import requests

# Step 1: Define the CSV file and columns to exclude (based on column names)
csv_file = 'sample.csv'  # Replace with your CSV file path
columns_to_exclude = ['column_1', 'column_3']  # Names of the columns to exclude

# Step 2: Read the CSV file, exclude the header and unwanted columns
csv_content = []
header = []

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    
    # Step 3: Read the header
    header = next(csv_reader)  # Read the header (first row)
    
    # Step 4: Filter the columns based on column names
    columns_to_keep = [col for col in header if col not in columns_to_exclude]
    
    # Step 5: Process each row and keep only the columns that are in `columns_to_keep`
    for row in csv_reader:
        filtered_row = [value for i, value in enumerate(row) if header[i] in columns_to_keep]
        csv_content.append(','.join(filtered_row))  # Rebuild the row as a CSV string

# Step 6: Combine all rows into a single CSV string (excluding unwanted columns)
csv_data = '\n'.join(csv_content)  # Join all rows with newline to create the final CSV data

# Step 7: Define the API endpoint (replace with your actual URL)
url = 'https://your-api-endpoint.com'  # Replace with your API endpoint

# Step 8: Send the raw CSV content in the POST request
headers = {
    'Content-Type': 'application/csv',  # Or 'text/csv', depending on your API's requirement
}

# Step 9: Send the POST request with the filtered CSV content
response = requests.post(url, data=csv_data, headers=headers)

# Step 10: Check the response
if response.status_code == 200:
    print(f"Success: {response.text}")
else:
    print(f"Failed: {response.status_code}, {response.text}")

#####################################################################
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
    for tag, value in xml_data.items():
        if isinstance(value, list):
            for item in value:
                # Flatten each item in the list (e.g., each RPT or TxId entry)
                flattened_row = flatten_dict(item, parent_key=f'{tag}')
                rows.append(flattened_row)
        else:
            # If it's not a list, it's a single element (handle it as a single row)
            flattened_row = flatten_dict(value, parent_key=f'{tag}')
            rows.append(flattened_row)

    return rows

import json
# Example function to process the table of XML data
def process_table_with_xml(df):
    # Create a list to store the new rows with additional columns from XML
    all_rows = []

    for index, row in df.iterrows():
        # Parse XML data from the current row (it assumes the XML data is in the 'xml_data' column)
        xml_data_str = row['xml_data']
        
        # Parse XML string into a dictionary
        xml_dict = xmltodict.parse(xml_data_str)
        
        # Extract the RcncltnRpt data from the parsed XML
        rcncltn_rpt = find_key(xml_dict, 'RcncltnRpt')

        # Flatten the XML data into rows
        flattened_data = flatten_xml_to_rows(rcncltn_rpt)

        # print(flattened_data, "78"*100)
        # print(row['uni_key'])
        # columns_to_exclude = ['xml_data', 'uni_key'] 
        # filtered_row = {key: value for key, value in row.to_dict().items() if key not in columns_to_exclude}
        # For each flattened row, combine with the original row (col1, col2)
        
        for data_row in flattened_data:
            columns_to_exclude = ['xml_data', 'uni_key'] 
            filtered_row = {key: value for key, value in row.to_dict().items() if key not in columns_to_exclude}
            extract_value = {}
            # print(row['uni_key'], "89"*100)
            for key in tuple(row['uni_key']):
                print(key)
                matching_keys = [actual_key for actual_key in data_row if key in actual_key]
                # print(matching_keys, "92"*100)
                # key = key.strip()
                # matching_keys = [actual_key for actual_key in data_row if key.lower() in actual_key.lower()]

                for matching_key in matching_keys:
                    extract_value[matching_key] = data_row[matching_key]
            # print(extract_value, "94"*100)
            if extract_value:
                uni_key_extrated_val = {'extract_value': extract_value}
                combined_row = {**filtered_row, **data_row, **uni_key_extrated_val}
            else:
                combined_row = {**filtered_row, **data_row}
            #combined_row = {**filtered_row, **data_row}
            all_rows.append(combined_row)

    # Convert the processed rows into a DataFrame
    print(json.dumps(all_rows), "83"*100)
    processed_df = pd.DataFrame(all_rows)

    return processed_df

# Sample input table with XML data
data = {
    'col1': ['abc'],
    'col2': [123],
    'uni_key': ["'UnqTxIdr', 'CtrctMtchgCrit_ISIN_Val2'"],
    'xml_data': [
        '''
        <RcncltnRpt>
            <TxId>
                <New>
                    <UnqTxIdr>new_NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
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
                </New>
            </TxId>
            <TxId>
                <Mod>
                    <UnqTxIdr>mod_NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
                    <CtrctMtchgCrit>
                        <ISIN>
                            <Val2>US9311421038</Val2>
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
                </Mod>
            </TxId>
        </RcncltnRpt>
        '''
    ]
}

df = pd.DataFrame(data)

# Process the table and extract XML data into new columns
processed_df = process_table_with_xml(df)

# Save the resulting DataFrame to CSV
processed_df.to_csv('process.csv', index=False)

# Show the resulting DataFrame to verify
# print(processed_df)




