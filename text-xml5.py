import xml.etree.ElementTree as ET


# def get_element_values(element):
#     """
#     Recursively collect text values from XML elements.
#     """
#     values = {}
#     for child in element:
#         if child.tag not in values:
#             values[child.tag] = child.text.strip() if child.text else ""
#         else:
#             if isinstance(values[child.tag], list):
#                 values[child.tag].append(child.text.strip() if child.text else "")
#             else:
#                 values[child.tag] = [values[child.tag], child.text.strip() if child.text else ""]
#         values.update(get_element_values(child))
#     return values

def get_element_values(element, prefix=""):
    """
    Recursively collect text values from XML elements.
    """
    values = {}
    for child in element:
        if child.tag not in values:
            values[child.tag] = child.text.strip() if child.text else ""
        else:
            if isinstance(values[child.tag], list):
                values[child.tag].append(child.text.strip() if child.text else "")
            else:
                values[child.tag] = [values[child.tag], child.text.strip() if child.text else ""]
        values.update(get_element_values(child, prefix=prefix))
    return values


# Load input XML files
input1 = """
<TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
    <CtrPtyId>
        <RptgCtrPty>
            <LEI>529900FDQEQ91XN3W228</LEI>
        </RptgCtrPty>
        <OthrCtrPty>
            <Lg1>
                <LEI>549300681JNVQWG2CM14</LEI>
            </Lg1>
        </OthrCtrPty>
        <RptSubmitgNtty>
            <LEI>5493004VCP8BLKLM5895</LEI>
        </RptSubmitgNtty>
        <NttyRspnsblForRpt>
            <LEI>52990069T419C3RYDL08</LEI>
        </NttyRspnsblForRpt>
    </CtrPtyId>
    <Tt1NbOfTxs>156</Tt1NbOfTxs>
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
</TxDtls>
"""

input2 = """
<TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
    <CtrPtyId>
        <RptgCtrPty>
            <LEI>529900FDQEQ91XN3W228</LEI>
        </RptgCtrPty>
        <OthrCtrPty>
            <Lg1>
                <LEI>549300681JNVQWG2CM14</LEI>
            </Lg1>
        </OthrCtrPty>
        <RptSubmitgNtty>
            <LEI>5493004VCP8BLKLM5895</LEI>
        </RptSubmitgNtty>
        <NttyRspnsblForRpt>
            <LEI>52990069T419C3RYDL08</LEI>
        </NttyRspnsblForRpt>
    </CtrPtyId>
    <Tt1NbOfTxs>156</Tt1NbOfTxs>
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
</TxDtls>
"""

# Parse the XML inputs
root1 = ET.fromstring(input1)
root2 = ET.fromstring(input2)

# Find UnqTxIdr in both XMLs
unq_tx_idr1 = root1.find('.//UnqTxIdr')
unq_tx_idr2 = root2.find('.//UnqTxIdr')

print(unq_tx_idr1, "106"*10)
print(unq_tx_idr2, "107"*10)

if unq_tx_idr1 is not None and unq_tx_idr2 is not None:
    # Logic to compare tags and their values
    result = {}

    for rcncltn_rpt in root1.findall('.//RcncltnRpt'):
        unq_tx_idr = rcncltn_rpt.find('.//UnqTxIdr').text
        print(unq_tx_idr, "117"*10)
        if unq_tx_idr == unq_tx_idr1.text:
            mtchg_crit = rcncltn_rpt.find('.//MtchgCrit')
            if mtchg_crit is not None:
                for child in mtchg_crit:
                    child_tag = child.tag
                    if child_tag not in result:
                        result[child_tag] = [sub_child.tag for sub_child in child]
                    else:
                        result[child_tag].extend(sub_child.tag for sub_child in child)

    print(result, "130"*10)

    # Check if tags match
    tags1 = list(result.keys())
    tags2 = list(result.keys())

    print(tags1, "$-"*10)
    print(tags2, "#-"*10)
    if tags1 == tags2:
        # Check tag values
        # results = []
        # uti = unq_tx_idr1.text
        
        # for tag in tags1:
        #     # # res = []
        #     # # for elem in root1.findall('.//RcncltnRpt//MtchgCrit//{}'.format(tag)):
        #     # #     print(elem, "140"*100)
        #     # #     print(elem.text.strip(), "142"*100)
        #     # #     res.append(elem.text.strip())
        #     # # print(res, "145-"*10)
        #     # eod_values = [elem.text.strip() if elem.text else "" for elem in root1.findall('.//RcncltnRpt//MtchgCrit//{}//Val1//Id'.format(tag))]
        #     # expect_values = [elem.text.strip() if elem.text else "" for elem in root2.findall('.//RcncltnRpt//MtchgCrit//{}//Val1//Id'.format(tag))]
        #     eod_values = get_element_values(root1.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     expect_values = get_element_values(root2.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     result_status = all(eod == expect for eod, expect in zip(eod_values, expect_values))
        #     results.append({
        #         "uti": uti,
        #         "tag_name": tag,
        #         "eod_{}_values".format(tag.lower()): eod_values,
        #         "expect_{}_values".format(tag.lower()): expect_values,
        #         "test_result": "pass" if result_status else "fail"
        #     })


        results = []
        uti = unq_tx_idr1.text

        # for tag in tags1:
        #     eod_values = get_element_values(root1.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     expect_values = get_element_values(root2.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     for key, value in eod_values.items():
        #         result_status = value == expect_values.get(key, "")
        #         results.append({
        #             "uti": uti,
        #             "tag_name": tag,
        #             "eod_{}_{}".format(tag.lower(), key.lower()): value,
        #             "expect_{}_{}".format(tag.lower(), key.lower()): expect_values.get(key, ""),
        #             "test_result": "pass" if result_status else "fail"
        #         })

        # for tag in tags1:
        #     eod_values = get_element_values(root1.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     expect_values = get_element_values(root2.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)))
        #     for key, value in eod_values.items():
        #         result_status = value == expect_values.get(key, "")
        #         if isinstance(value, list):
        #             for i, val in enumerate(value):
        #                 results.append({
        #                     "uti": uti,
        #                     "tag_name": tag,
        #                     "eod_{}_{}".format(tag.lower(), key.lower()): val,
        #                     "expect_{}_{}".format(tag.lower(), key.lower()): expect_values.get(key, "")[i] if isinstance(expect_values.get(key, ""), list) else expect_values.get(key, ""),
        #                     "test_result": "pass" if result_status else "fail"
        #                 })
        #         else:
        #             results.append({
        #                 "uti": uti,
        #                 "tag_name": tag,
        #                 "eod_{}_{}".format(tag.lower(), key.lower()): value,
        #                 "expect_{}_{}".format(tag.lower(), key.lower()): expect_values.get(key, ""),
        #                 "test_result": "pass" if result_status else "fail"
        #             })

        for tag in tags1:
            eod_values = get_element_values(root1.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)), prefix="eod_{}_".format(tag.lower()))
            expect_values = get_element_values(root2.find('.//RcncltnRpt//MtchgCrit//{}'.format(tag)), prefix="expect_{}_".format(tag.lower()))
            for key, value in eod_values.items():
                result_status = value == expect_values.get(key, "")
                if isinstance(value, list):
                    for i, val in enumerate(value):
                        results.append({
                            "uti": uti,
                            "tag_name": tag,
                            "{}{}".format("eod_{}_".format(tag.lower()), key.lower()): val,
                            "{}{}".format("expect_{}_".format(tag.lower()), key.lower()): expect_values.get(key, "")[i] if isinstance(expect_values.get(key, ""), list) else expect_values.get(key, ""),
                            "test_result": "pass" if result_status else "fail"
                        })
                else:
                    results.append({
                        "uti": uti,
                        "tag_name": tag,
                        "{}{}".format("eod_{}_".format(tag.lower()), key.lower()): value,
                        "{}{}".format("expect_{}_".format(tag.lower()), key.lower()): expect_values.get(key, ""),
                        "test_result": "pass" if result_status else "fail"
                    })





            print(results)
    else:
        print("Tags do not match.")
else:
    print("UnqTxIdr not found in both XMLs.")




