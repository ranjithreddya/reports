import xml.etree.ElementTree as ET

# Sample XML input
xml_data = '''<RPT xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
    <RcnltnCtgrs>
        <RptgRqrmnt>
            <RptgTp>TWOS</RptgTp>
            <Pairg>PARD</Pairg>
            <Rcncltn>NREC</Rcncltn>
            <ValtnRcncltn>NOAP</ValtnRcncltn>
            <Rvvd>false</Rvvd>
            <FrthrMod>true</FrthrMod>
        </RptgRqrmnt>
    </RcnltnCtgrs>
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>529900FDQEQ91XN3W228</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>549300681JNVQWG2CM14</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR93</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK040824243049TC99999SEUREFIT516115XCOMNEGR964</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>NK0408242430490000000000000000000000000</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
    <RcnltnCtgrs>
        <RptgRqrmnt>
            <RptgTp>TWOS</RptgTp>
            <Pairg>PARD</Pairg>
            <Rcncltn>NREC</Rcncltn>
            <ValtnRcncltn>NOAP</ValtnRcncltn>
            <Rvvd>false</Rvvd>
            <FrthrMod>true</FrthrMod>
        </RptgRqrmnt>
    </RcnltnCtgrs>
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>549300681JNVQWG2CM14</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>529900FDQEQ91XN3W228</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>11111111111111111111111111111111111111111Ranjith</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                <RptgCtrPty>
                    <LEI>549300681JNVQWG2CM14</LEI>
                </RptgCtrPty>
                <OthrCtrPty>
                    <Lg1>
                        <LEI>529900FDQEQ91XN3W228</LEI>
                    </Lg1>
                </OthrCtrPty>
                <RptSubmitgNtty>
                    <LEI>5493004VCP8BLKLM5895</LEI>
                </RptSubmitgNtty>
                <NttyRspnsblForRpt>
                    <LEI>52990069T419C3RYDL08</LEI>
                </NttyRspnsblForRpt>
            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
    <RcnltnCtgrs>
        <RptgRqrmnt>
            <RptgTp>TWOS</RptgTp>
            <Pairg>PARD0</Pairg>
            <Rcncltn>NREC</Rcncltn>
            <ValtnRcncltn>NOAP</ValtnRcncltn>
            <Rvvd>false</Rvvd>
            <FrthrMod>true</FrthrMod>
        </RptgRqrmnt>
    </RcnltnCtgrs>
    <Txdtl>
        <CtrPtyId>
            <RptgCtrPty>
                <LEI>1111111111111111</LEI>
            </RptgCtrPty>
            <OthrCtrPty>
                <Lg1>
                    <LEI>222222222222222222</LEI>
                </Lg1>
            </OthrCtrPty>
        </CtrPtyId>
        <RcncltnRpt>
            <TxId>
                <UnqIdr>
                    <UnqTxIdr>11111111111111111111111111111111111111111</UnqTxIdr>
                </UnqIdr>
            </TxId>
            <MtchgCrit>
                            </MtchgCrit>
        </RcncltnRpt>
    </Txdtl>
</RPT>'''

# Parse the XML
root = ET.fromstring(xml_data)

# Define the replacement function
def replace_unqtxidr(unqtxidr):
    if unqtxidr.startswith('NK') or unqtxidr.startswith('AK'):
        return unqtxidr[:2] + 'ranjith' + unqtxidr[14:]
    return unqtxidr

# Iterate through all UnqTxIdr elements and replace their values
for unqtxidr in root.findall('.//UnqTxIdr'):
    old_value = unqtxidr.text
    new_value = replace_unqtxidr(old_value)
    unqtxidr.text = new_value

# Output the modified XML
new_xml_data = ET.tostring(root, encoding='unicode')

print(new_xml_data)



import pandas as pd
from deepdiff import DeepDiff
import io

# Define the CSV data as strings
csv1 = """
c1,xml,c3,c4
NKranjithTC99999SEUREFIT51547XCOMNEGR93,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM14</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W228</LEI> <LEI>529900FDQEQ91XN3W214</LEI>
NKranjithTC99999SEUREFIT516115XCOMNEGR964,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM14</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W214</LEI> <LEI>529900FDQEQ91XN3W228</LEI>
NKranjithTC99999SEUREFIT516115XCOMNEGR961,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM15</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W214</LEI> <LEI>529900FDQEQ91XN3W228</LEI>
"""

csv2 = """
c1,xml,c3,c4
NKranjithTC99999SEUREFIT51547XCOMNEGR93,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM14</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W228</LEI> <LEI>529900FDQEQ91XN3W214</LEI>
NKranjithTC99999SEUREFIT516115XCOMNEGR964,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM14</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W214</LEI> <LEI>529900FDQEQ91XN3W228</LEI>
NKranjithTC99999SEUREFIT516115XCOMNEGR962,<MtchgCrit><RptgCtrPty><LEI>549300681JNVQWG2CM16</LEI></RptgCtrPty></MtchgCrit> <LEI>529900FDQEQ91XN3W214</LEI> <LEI>529900FDQEQ91XN3W228</LEI>
"""

# Read CSV data into DataFrames using io.StringIO
df1 = pd.read_csv(io.StringIO(csv1))
df2 = pd.read_csv(io.StringIO(csv2))

# Merge DataFrames on 'c1', 'c3', 'c4' using an outer join
merged_df = pd.merge(df1, df2, on=['c1', 'c3', 'c4'], how='outer', suffixes=('_csv1', '_csv2'))

# Construct the output dictionary
output = {}
for index, row in merged_df.iterrows():
    key = row['c1']
    xml_csv1 = row['xml_csv1'] if 'xml_csv1' in row and pd.notnull(row['xml_csv1']) else ''
    xml_csv2 = row['xml_csv2'] if 'xml_csv2' in row and pd.notnull(row['xml_csv2']) else ''
    output[key] = {
        "xml1": xml_csv1,
        "xml2": xml_csv2
    }

# Print the output
print(output)
# Loop through the dictionary and print the details
for key, value in xml_data.items():
    print(f"Key: {key}")
    print(f"XML from csv1: {value['xml1']}")
    print(f"XML from csv2: {value['xml2']}")
    print("-" * 40)

###########################################################################

import pandas as pd

# Snowflake table data
data = {
    'sub_id': ['s1', 's2', 's3', 's4'],
    'date': ['2024-05-26', '2024-05-27', '2024-05-26', '2024-05-27']
}

# Load into DataFrame
snowflake_df = pd.DataFrame(data)

# Input array
input_array = [
    {"sid": "s1", "csv_path": "test1.csv"},
    {"sid": "s2", "csv_path": "test2.csv"},
    {"sid": "s3", "csv_path": "test3.csv"},
    {"sid": "s4", "csv_path": "test4.csv"}
]

# Convert input array to DataFrame
input_df = pd.DataFrame(input_array)

# Merge data on 'sub_id'
merged_df = pd.merge(snowflake_df, input_df, left_on='sub_id', right_on='sid')

# Display the result
for _, row in merged_df.iterrows():
    print(f"Date: {row['date']}, CSV Path: {row['csv_path']}")


import pandas as pd
from io import StringIO

# Sample CSV data
csv_data = """uti, test1_abc, test4_dge, test3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93, test1_value, test2_contains, test3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93, test1_contains, , test3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93, test1_value, test2_value, test3_contains"""

# Load the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# Input list of columns to apply the replacement
input_columns = ['test']
replacement_value = 'updated'

# Apply the conditions to DataFrame columns specified in input_columns
for column in df.columns:
    # Check if the column name should be processed
    for input_column in input_columns:
        if input_column in column:
            df.loc[df[column].str.contains(input_column, na=False), column] = replacement_value

# Print the modified DataFrame
print(df.to_csv(index=False))




import pandas as pd
from io import StringIO

# Sample CSV data
csv_data = """uti,test1_abc,test4_dge,test3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93,1_value,2_contains,3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93,1_contains,,3_dnn
NK040824243049TC99999SEUREFIT51547XCOMNEGR93,1_value,2_value, 3_contains"""

# Load the CSV data into a DataFrame
df = pd.read_csv(StringIO(csv_data))

# The substring to search for in column names
substring = 'test'

# Define the new value to use for non-NaN and non-empty values
new_value = 'updated'

# Iterate over columns that contain the substring
for column in df.columns:
    if substring in column:
        # Update only non-NaN and non-empty values
        df[column] = df[column].apply(lambda x: new_value if pd.notna(x) and x != '' else x)

import os

latest_dir = max((os.path.join('/path/to/your/directory', d) for d in os.listdir('/path/to/your/directory') if os.path.isdir(os.path.join('/path/to/your/directory', d))), key=os.path.getmtime, default=None)
