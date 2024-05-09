# import csv
# import xml.etree.ElementTree as ET
# import json
# from deepdiff import DeepDiff
# import xmltodict

# from ordered_set import OrderedSet

# xml_src = "/Users/ranjithrreddyabbidi/ranjith/xml1.xml"
# xml_target = "/Users/ranjithrreddyabbidi/ranjith/xml2.xml"
# xml_final_op = f'/Users/ranjithrreddyabbidi/ranjith'
# print("DEBUGGG")
# tree=ET.parse(xml_src)

# root=tree.getroot()

# tree1=ET.parse(xml_target)

# root1=tree1.getroot()
# xmlstr1 = ET.tostring (root, encoding='utf-8', method='xml').decode() 
# xmlstr2 = ET.tostring (root1, encoding='utf-8', method='xml').decode() 

# xmlstr1 = xmlstr1.replace('ns0:','')
# xmlstr2=xmlstr2.replace('ns0:','')

# print("DEBUGGG")

# def serialize(obj):
#     if isinstance(obj, OrderedSet):
#         return list(obj)
#     elif isinstance(obj, dict):
#         return {key: serialize(value) for key, value in obj.items()}
#     elif isinstance(obj, (list, tuple)):
#         return [serialize(item) for item in obj]
#     return obj

# src_json = xmltodict.parse (xmlstr1)
# print("DEBUGGG")
# target_json=xmltodict.parse(xmlstr2)
# print(src_json)
# print (target_json)
# diff=DeepDiff(src_json,target_json)
# print("*"*100)
# print (diff)
# print(json.dumps(diff, default=serialize))

# data_str = json.dumps(diff, default=serialize)

# try:
#     # Try to load the string as JSON
#     data = json.loads(data_str)
# except json.JSONDecodeError:
#     # If it's not in JSON format, assume it's already a dictionary
#     data = eval(data_str)

# output = {}
# for key, value in data.items():
#     if key == 'dictionary_item_added':
#         tagname = value[0].split("'")[-2]
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = None
#         output['Except'] = None
#         output['test-result'] = 'fail'
#     else:
#         nested_key = list(value.keys())[0]  # Get the nested key
#         tagname = nested_key.split("'")[-2]  # Extract the tagname from the nested key
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = value[nested_key]['new_value']
#         output['Except'] = value[nested_key]['old_value']
#         output['test-result'] = 'fail'


# print(output)
# ###################################################################



import re

input_string = "root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']"

# Define a regular expression pattern to match and capture the desired substring
pattern = r"'MtchgCrit'\]\['([^']+)'\]\['([^']+)'\]\['([^']+)'\](.*)"

# Search for the pattern in the input string
match = re.search(pattern, input_string)

if match:
    groups = match.groups()
    output_string = "<" + "><".join(groups[:-1]) + ">"
    print(output_string)
else:
    print("Pattern not found")


# {"dictionary_item_added": ["root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['CtrctMtchgCrit']['ISIN']"], "values_changed": {"root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']": {"new_value": "AAP", "old_value": "AAPA"}}}




# if key == 'dictionary_item_added':

# 	result = {tagname :'<CtrctMtchgCrit><ISIN>'
# 	eod : null
# 	Except : 
# 	test-result : fail}
# else:
# 	result = {tagname :'<TxMtchgCrit><PltfmIdr><Val1>'
# 	eod : AAP
# 	Except : AAPA
# 	test-result : fail}

