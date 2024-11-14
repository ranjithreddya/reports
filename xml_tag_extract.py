import re
# Input XML string
xml_data = """
<RPT>
    <RcncltnRpt>
        <TxId>
            <UnqIdr>
                <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR91</UnqTxIdr>
            </UnqIdr>
        </TxId>
        <MtchgCrit>
        </MtchgCrit>
    </RcncltnRpt>
    <RcncltnRpt>
        <TxId>
            <UnqIdr>
                <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR92</UnqTxIdr>
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
                <UnqTxIdr>NK040824243049TC99999SEUREFIT51547XCOMNEGR94</UnqTxIdr>
            </UnqIdr>
        </TxId>
        <MtchgCrit>
        </MtchgCrit>
    </RcncltnRpt>
</RPT>
"""

# Target UnqTxIdr to search for
target_unqtxidr = "NK040824243049TC99999SEUREFIT51547XCOMNEGR94"

# # Directly extract the block based on known positions
# start_marker = f"<UnqTxIdr>{target_unqtxidr}</UnqTxIdr>"
# end_marker = "</RcncltnRpt>"

# # Manually define where the start and end of the block should be
# # This is done by directly cutting based on the target value position
# start_idx = xml_data.find(start_marker)
# print(start_idx)
# if start_idx != -1:
#     # Assuming the <RcncltnRpt> block starts just before the <UnqTxIdr> and ends with </RcncltnRpt>
#     block_start = xml_data.rfind("<RcncltnRpt>", 0, start_idx)
#     block_end = xml_data.find(end_marker, start_idx) + len(end_marker)

#     # Directly slice the string for the matching block
#     matching_block = xml_data[block_start:block_end]
#     print(matching_block)



pattern = r"<RcncltnRpt>.*?<UnqTxIdr>{}</UnqTxIdr>.*?</RcncltnRpt>".format(re.escape(target_unqtxidr))

# Use re.DOTALL to allow dot to match newlines
match = re.search(pattern, xml_data, re.DOTALL)

# If a match is found, print the matched XML block
if match:
    print(match.group(0))
else:
    print("No matching block found.")
