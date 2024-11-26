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

######################################################

final_output = []

# Iterate over each entity in the data["entities"]
for entity in data["entities"]:
    # Create a dictionary to store the values for each entity
    entity_dict = {
        "JIRA": None,
        "TCID": None,
        "Component": None,
        "Apllication": None,
        "Release": None
    }
    
    # Iterate over each field in the entity's "Fields"
    for field in entity["Fields"]:
        field_name = field["Name"]
        field_value = field["Values"][0]["value"] if field["Values"] else None
        
        # Map the specific fields to the required keys
        if field_name == "user-07":
            entity_dict["JIRA"] = field_value
        elif field_name == "id":
            entity_dict["TCID"] = field_value
        elif field_name == "user-02":
            entity_dict["Component"] = field_value
        elif field_name == "user-10":
            entity_dict["Apllication"] = field_value
        elif field_name == "user-04":
            entity_dict["Release"] = field_value
    
    # Append the created dictionary for this entity to the final_output
    final_output.append(entity_dict)



