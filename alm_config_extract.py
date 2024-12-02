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

################################################################


try:
    # Input data with multiple entities
    data = {
        "entities": [
            {
                "Fields": [
                    {"Name": "user-07", "Values": [{"value": "JFSA-07"}]},
                    {"Name": "id", "Values": [{"value": "67462"}]},
                    {"Name": "user-10", "Values": [{}]},
                    {"Name": "user-04", "Values": [{"value": "JFSA-04"}]},
                    {"Name": "user-02", "Values": [{"value": "JFSA-02"}]}
                ]
            },
            {
                "Fields": [
                    {"Name": "user-07", "Values": [{"value": "07"}]},
                    {"Name": "id", "Values": [{"value": "67461"}]},
                    {"Name": "user-10", "Values": [{"value": "10"}]},
                    {"Name": "user-04", "Values": [{"value": "04"}]},
                    {"Name": "user-02", "Values": [{"value": "02"}]}
                ]
            }
        ]
    }

    # Process entities and dynamically map the fields
    final_output = [
        {
            # Dynamically map the user-<number> fields to the required keys
            "JIRA": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-07"), None),
            "TCID": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "id"), None),
            "Component": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-02"), None),
            "Apllication": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-10"), None),
            "Release": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-04"), None)
        }
        for entity in data["entities"]
    ]

    # Print the final output
    print(final_output)

except Exception as e:
    import traceback
    traceback.print_exc()


######################################################################################
final_output = [
    {
        "JIRA": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-07" and field.get("Values")), None),
        "TCID": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "id" and field.get("Values")), None),
        "Component": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-02" and field.get("Values")), None),
        "Application": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-10" and field.get("Values")), None),
        "Release": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-04" and field.get("Values")), None)
    }
    for entity in data["entities"]
]

##########################################################################


import json
from django.db import transaction
from .models import ALM_TEST_DATA  # Adjust this import according to your project structure

# Load the JSON file
try:
    with open('file.json', 'r') as file:
        file_data = file.read()

    data = json.loads(file_data)

    # Process the data and map fields dynamically
    final_output = [
        {
            "JIRA": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-07" and field.get("Values")), None),
            "TCID": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "id" and field.get("Values")), None),
            "Component": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-02" and field.get("Values")), None),
            "Application": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-10" and field.get("Values")), None),
            "Release": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-04" and field.get("Values")), None)
        }
        for entity in data["entities"]
    ]

    # Prepare instances for bulk_create
    instances = [
        ALM_TEST_DATA(
            JIRA=item['JIRA'],
            TCID=item['TCID'],
            Component=item['Component'],
            Application=item['Application'],
            Release=item['Release']
        )
        for item in final_output
    ]

    # Function to insert data in batches to avoid exceeding DB limits
    def bulk_insert_in_batches(instances, batch_size=10000):
        for i in range(0, len(instances), batch_size):
            batch = instances[i:i + batch_size]
            try:
                # Use Django's bulk_create to insert a batch of records
                ALM_TEST_DATA.objects.bulk_create(batch)
                print(f"Inserted {len(batch)} records.")
            except Exception as e:
                print(f"Error inserting batch {i // batch_size + 1}: {e}")
                raise  # Reraise the exception if you want to handle it globally

    # Run the bulk insert in batches
    bulk_insert_in_batches(instances)

except Exception as e:
    import traceback
    traceback.print_exc()



##################################################################
import json
from django.db import transaction
from .models import ALM_TEST_DATA  # Adjust this import according to your project structure

# Load the JSON file
try:
    with open('file.json', 'r') as file:
        file_data = file.read()

    data = json.loads(file_data)

    # Process the data and map fields dynamically
    final_output = [
        {
            "JIRA": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-07" and field.get("Values")), None),
            "TCID": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "id" and field.get("Values")), None),
            "Component": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-02" and field.get("Values")), None),
            "Application": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-10" and field.get("Values")), None),
            "Release": next((field["Values"][0].get("value") for field in entity["Fields"] if field["Name"] == "user-04" and field.get("Values")), None)
        }
        for entity in data["entities"]
    ]

    # Step 1: Gather all existing TCIDs in the database
    existing_records = ALM_TEST_DATA.objects.filter(TCID__in=[item['TCID'] for item in final_output])

    # Step 2: Create a dictionary of existing records by TCID
    existing_dict = {record.TCID: record for record in existing_records}

    # Step 3: Prepare lists for creating and updating
    records_to_create = []
    records_to_update = []

    # Step 4: Loop through incoming data and decide whether to create or update
    for item in final_output:
        jira = item['JIRA']
        tcid = item['TCID']
        component = item['Component']
        application = item['Application']
        release = item['Release']

        # Check if this TCID already exists
        if tcid in existing_dict:
            # If it exists, update the record
            existing_record = existing_dict[tcid]
            existing_record.JIRA = jira
            existing_record.Component = component
            existing_record.Application = application
            existing_record.Release = release
            records_to_update.append(existing_record)
        else:
            # If it doesn't exist, add a new record to create
            records_to_create.append(ALM_TEST_DATA(
                JIRA=jira,
                TCID=tcid,
                Component=component,
                Application=application,
                Release=release
            ))

    # Function to handle both updates and inserts in batches
    def bulk_insert_and_update_in_batches(records_to_create, records_to_update, batch_size=10000):
        for i in range(0, max(len(records_to_create), len(records_to_update)), batch_size):
            create_batch = records_to_create[i:i + batch_size]
            update_batch = records_to_update[i:i + batch_size]

            try:
                # Perform bulk create for the batch of records to be inserted
                if create_batch:
                    ALM_TEST_DATA.objects.bulk_create(create_batch)
                    print(f"Inserted {len(create_batch)} records.")

                # Perform bulk update for the batch of records to be updated
                if update_batch:
                    ALM_TEST_DATA.objects.bulk_update(update_batch, ['JIRA', 'Component', 'Application', 'Release'])
                    print(f"Updated {len(update_batch)} records.")

            except Exception as e:
                print(f"Error processing batch {i // batch_size + 1}: {e}")
                raise  # Reraise the exception if you want to handle it globally

    # Step 5: Perform bulk create and bulk update in batches
    bulk_insert_and_update_in_batches(records_to_create, records_to_update)

except Exception as e:
    import traceback
    traceback.print_exc()


###############################################################
from django.db import transaction
from .models import YourModel

def bulk_upload(data):
    # Step 1: Gather all existing tcids in the database
    existing_records = YourModel.objects.filter(tcid__in=[int(item['tcid']) for item in data])
    
    # Step 2: Create a dictionary of existing records by tcid
    existing_dict = {record.tcid: record for record in existing_records}
    
    # Step 3: Prepare lists for creating and updating
    records_to_create = []
    records_to_update = []

    # Step 4: Loop through incoming data and decide whether to create or update
    for item in data:
        jira = item['jira']
        tcid = int(item['tcid'])
        aid = int(item['aid'])

        # Check if this tcid already exists
        if tcid in existing_dict:
            # If it exists, update the record
            existing_record = existing_dict[tcid]
            existing_record.jira = jira
            existing_record.aid = aid
            records_to_update.append(existing_record)
        else:
            # If it doesn't exist, add a new record to create
            records_to_create.append(YourModel(jira=jira, tcid=tcid, aid=aid))
    
    # Step 5: Perform bulk update (if any)
    if records_to_update:
        YourModel.objects.bulk_update(records_to_update, ['jira', 'aid'])
    
    # Step 6: Perform bulk create (if any)
    if records_to_create:
        YourModel.objects.bulk_create(records_to_create)





