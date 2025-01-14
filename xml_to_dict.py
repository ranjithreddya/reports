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
    """
    Flattens a nested dictionary into a single level dictionary by joining nested keys.
    """
    items = []
    print(d, "29"*100)
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

def flatten_xml_to_rows(xml_data):
    """
    Handles nested XML data and flattens it into a list of rows, each as a dictionary.
    """
    if xml_data is None:
        return []  # Return an empty list if the XML data is None

    rows = []
    if isinstance(xml_data, dict):
        print(xml_data, "50"*100)
        for tag, value in xml_data.items():
            if isinstance(value, list):
                for item in value:
                    print(item, "53"*100)
                    flattened_row = flatten_dict(item, parent_key=f'{tag}')
                    rows.append(flattened_row)
            else:
                print(value, "57"*100)
                flattened_row = flatten_dict(value, parent_key=f'{tag}')
                rows.append(flattened_row)
    elif isinstance(xml_data, list):
        print(xml_data, "62"*100)
        for item in xml_data:
            print(item, "62"*100)
            flattened_row = flatten_dict(item, parent_key=f'{tag}')
            rows.append(flattened_row)

    return rows

def process_table_with_xml(df):
    """
    Process the input DataFrame by parsing and flattening XML data from the columns 'actual_xml' and 'expect_xml'.
    For each Report Type, create separate files for actual and expected data.
    """
    all_actual_rows = []
    all_expected_rows = []

    # Group by Report Type to process each report type batch
    for report_type, group in df.groupby('Report Type'):
        print(f"Processing report type: {report_type}")  # Add debug statement
        
        actual_rows = []
        expected_rows = []

        for _, row in group.iterrows():
            # Parse actual XML data from the current row
            actual_xml_str = row['actual_xml']
            expect_xml_str = row['expect_xml']
            identifier = row['identifier']
            
            try:
                # Parse both actual and expected XML strings into dictionaries
                actual_xml_dict = xmltodict.parse(actual_xml_str)
                expect_xml_dict = xmltodict.parse(expect_xml_str)
                
                # Print the parsed XML for debugging
                print(f"Parsed Actual XML for row {row['col1']}:", actual_xml_dict)
                print(f"Parsed Expected XML for row {row['col1']}:", expect_xml_dict)
                
                # Extract the identifier data from the parsed XML (dynamic based on identifier)
                actual_data = find_key(actual_xml_dict, identifier)
                expect_data = find_key(expect_xml_dict, identifier)

                
                # Skip if actual_data or expect_data is None
                if actual_data is None:
                    print(f"Actual data for {identifier} is None. Skipping.")  # Debug print
                if expect_data is None:
                    print(f"Expected data for {identifier} is None. Skipping.")  # Debug print


                print(actual_data, "98"*100)
                print(expect_data, "98"*100)
                
                # Flatten actual and expected XML data
                actual_flattened_data = flatten_xml_to_rows(actual_data) if actual_data else []
                expect_flattened_data = flatten_xml_to_rows(expect_data) if expect_data else []

                print(actual_flattened_data, "110"*100)
                print(expect_flattened_data, "111"*100)

                # For actual data rows, add to actual_rows with 'Data_Type' as 'Actual'
                for data_row in actual_flattened_data:
                    if 'TxId_UnqTxIdr' in data_row and data_row['TxId_UnqTxIdr'] is None:
                        data_row['TxId_UnqTxIdr'] = row['col3']
                    
                    # Add a flag to distinguish "Actual" data
                    data_row['Data_Type'] = 'Actual'
                    
                    # Combine the original row data (col1, col2, etc.) with the flattened XML data
                    combined_row = row.to_dict()  # Start with the original row as a dictionary
                    combined_row.update(data_row)  # Merge the flattened XML data into the original row
                    
                    # Add the combined row to the list of actual rows
                    actual_rows.append(combined_row)
                
                # For expected data rows, add to expected_rows with 'Data_Type' as 'Expected'
                for data_row in expect_flattened_data:
                    if 'TxId_UnqTxIdr' in data_row and data_row['TxId_UnqTxIdr'] is None:
                        data_row['TxId_UnqTxIdr'] = row['col3']
                    
                    # Add a flag to distinguish "Expected" data
                    data_row['Data_Type'] = 'Expected'
                    
                    # Combine the original row data (col1, col2, etc.) with the flattened XML data
                    combined_row = row.to_dict()  # Start with the original row as a dictionary
                    combined_row.update(data_row)  # Merge the flattened XML data into the original row
                    
                    # Add the combined row to the list of expected rows
                    expected_rows.append(combined_row)

            except Exception as e:
                print(f"Error processing row {row['col1']} ({row['col2']}): {e}")

        # Convert the actual and expected rows into DataFrames
        actual_report_type_df = pd.DataFrame(actual_rows)
        expected_report_type_df = pd.DataFrame(expected_rows)

        # Save the resulting DataFrames for actual and expected data to CSV
        actual_report_type_df.to_csv(f'{report_type}_actual_report_type.csv', index=False)
        expected_report_type_df.to_csv(f'{report_type}_expected_report_type.csv', index=False)

        # Append to the overall list (optional: can be used for further operations)
        all_actual_rows.extend(actual_rows)
        all_expected_rows.extend(expected_rows)
    
    # Return the processed DataFrames (optional)
    return pd.DataFrame(all_actual_rows), pd.DataFrame(all_expected_rows)


data = {
    'col1': ['abc', 'def', 'ghj', 'ijk', 'lmn', 'opq'],
    'col2': [123, 456, 789, 101, 112, 131],
    'col3': ['XYZ', 'ABC', 'DEF', 'GHI', 'JKL', 'MNO'],
    'Report Type': ['ranjith', 'alekya', 'alekya', 'ranjith', 'alekya', 'alekya'],
    'actual_xml': [
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr></UnqTxIdr>
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
    ],
    'expect_xml': [
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ123</UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ456</UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ789</UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ101</UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ111</UnqTxIdr>
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
        </RcncltnRpt>''',
        
        '''<RcncltnRpt>
            <TxId>
                <UnqTxIdr>XYZ200</UnqTxIdr>
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
    ],
    'identifier': ['TxId', 'TxId', 'TxId', 'TxId', 'TxId', 'TxId']
}




# Create a DataFrame from the data
df = pd.DataFrame(data)

# Process the DataFrame
actual_df, expected_df = process_table_with_xml(df)
