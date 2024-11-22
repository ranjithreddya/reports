import xml.etree.ElementTree as ET
import json

# XML string
xml_data = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?> 
<Entities TotalResults="60253">
    <Entity Type="test-config">
        <ChildrenCount>
            <Value>0</Value>
        </ChildrenCount>
        <Fields>
            <Field Name="last-modified">
                <Value>2024-11-14 02:41:20</Value>
            </Field>
            <Field Name="name">
                <Value>HKMA Remarks 1_IR STD_InterestRateCrossCurr</Value>
            </Field>
            <Field Name="id">
                <Value>1001</Value>
            </Field>
            <Field Name="parent-id">
                <Value>1</Value>
            </Field>
        </Fields>
    </Entity>
    <Entity Type="test-config">
        <ChildrenCount>
            <Value>0</Value>
        </ChildrenCount>
        <Fields>
            <Field Name="last-modified">
                <Value>2024-11-14 02:41:20</Value>
            </Field>
            <Field Name="name">
                <Value>HKMA Remarks 1_IR</Value>
            </Field>
            <Field Name="id">
                <Value>1002</Value>
            </Field>
            <Field Name="parent-id">
                <Value>2</Value>
            </Field>
        </Fields>
    </Entity>
</Entities>'''

# Parse the XML
root = ET.fromstring(xml_data)

# Extract the data
entities = []
for entity in root.findall('Entity'):
    fields = entity.find('Fields')
    entity_data = {}
    for field in fields.findall('Field'):
        field_name = field.get('Name')
        field_value = field.find('Value').text
        entity_data[field_name] = field_value
    entities.append(entity_data)

# Convert to JSON
json_data = json.dumps(entities, indent=2)
print(json_data)
