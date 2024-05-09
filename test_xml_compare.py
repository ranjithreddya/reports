from xml.etree import ElementTree as ET
from deepdiff import DeepDiff

# Function to extract UnqTxIdr value from XML element
def extract_unqtxidr(xml_element):
    return xml_element.find('.//UnqTxIdr').text

# Function to extract MtchgCrit section from XML element
def extract_mtchgcrit(xml_element):
    mtchg_crit_element = xml_element.find('.//MtchgCrit')
    return ET.tostring(mtchg_crit_element, encoding='unicode')

# XML strings
input_xml_str = '''<TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
    ...
</TxDtls>'''

target_xml_str = '''<TxDtls xmlns:ns0="urn:iso:std:iso:20022:tech:xsd:head.091.001.02">
    ...
</TxDtls>'''

# Parse XML strings
input_xml = ET.fromstring(input_xml_str)
target_xml = ET.fromstring(target_xml_str)

# Extract UnqTxIdr values
input_unqtxidr = extract_unqtxidr(input_xml)
target_unqtxidr = extract_unqtxidr(target_xml)

# Check if UnqTxIdr values match
if input_unqtxidr == target_unqtxidr:
    print("UnqTxIdr values match.")
    
    # Extract MtchgCrit sections
    input_mtchgcrit = extract_mtchgcrit(input_xml)
    target_mtchgcrit = extract_mtchgcrit(target_xml)
    
    # Generate deep difference in MtchgCrit sections
    mtchgcrit_diff = DeepDiff(input_mtchgcrit, target_mtchgcrit)
    print("MtchgCrit difference:")
    print(mtchgcrit_diff)
else:
    print("UnqTxIdr values do not match.")



########################################################################################################

import csv
import xml.etree.ElementTree as ET
import json
from deepdiff import DeepDiff
import xmltodict


xml_src = "/Users/ranjithrreddyabbidi/ranjith/xml1.xml"
xml_target = "/Users/ranjithrreddyabbidi/ranjith/xml2.xml"
xml_final_op = f'/Users/ranjithrreddyabbidi/ranjith'
print("DEBUGGG")
tree=ET.parse(xml_src)

root=tree.getroot()

tree1=ET.parse(xml_target)

root1=tree1.getroot()
xmlstr1 = ET.tostring (root, encoding='utf-8', method='xml').decode() 
xmlstr2 = ET.tostring (root1, encoding='utf-8', method='xml').decode() 

xmlstr1 = xmlstr1.replace('ns0:','')
xmlstr2=xmlstr2.replace('nso:','')

print("DEBUGGG")

src_json = xmltodict.parse (xmlstr1)
print("DEBUGGG")
target_json=xmltodict.parse(xmlstr2)
print(src_json)
print (target_json)
diff=DeepDiff(src_json,target_json)
print (diff)
print(json.dumps(diff))
