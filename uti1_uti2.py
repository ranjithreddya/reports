# Define a function to extract the namespace from an element's tag
def get_namespace(element):
    if '}' in element.tag:
        return element.tag.split('}')[0][1:]
    else:
        return ''

# Get namespace from the root element of the first XML document
ns_map = {get_namespace(root1): None}

# Revised comparison logic
if unq_tx_idr1 is not None and unq_tx_idr2 is not None:
    results = []
    uti1 = unq_tx_idr1.text
    uti2 = unq_tx_idr2.text

    # Compare values under <MtchgCrit> for each <UnqTxIdr>
    for unq_tx_idr in [unq_tx_idr1, unq_tx_idr2]:
        mtchg_crit = unq_tx_idr.find('.//{namespace}*//MtchgCrit'.format(namespace=list(ns_map.keys())[0]))
        if mtchg_crit is not None:
            eod_values = get_element_values(mtchg_crit)
            # Identify the corresponding UTI
            uti = uti1 if unq_tx_idr == unq_tx_idr1 else uti2
            for tag, values in eod_values.items():
                expect_values = get_element_values(root2.find('.//{namespace}*//UnqTxIdr[text()="{text}"]//MtchgCrit/{tag}'.format(namespace=list(ns_map.keys())[0], text=unq_tx_idr2.text, tag=tag)))
                for key, value in values.items():
                    expect_value = expect_values.get(key, "")
                    result_status = value == expect_value
                    results.append({
                        "uti": uti,
                        "tag_name": tag,
                        "eod_{}_{}".format(tag.lower(), key.lower()): value,
                        "expect_{}_{}".format(tag.lower(), key.lower()): expect_value,
                        "test_result": "pass" if result_status else "fail"
                    })
    print(results)
else:
    print("UnqTxIdr not found in both XMLs.")
