# Input data with multiple entities
data = {
    "entities": [
        {
            "Fields": [
                {"Name": "user-07", "Values": [{"value": "JFSA-07"}]},
                {"Name": "id", "Values": [{"value": "67462"}]},
                {"Name": "user-10", "Values": [{"value": "JFSA-10"}]},
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
        "JIRA": next((field["Values"][0]["value"] for field in entity["Fields"] if field["Name"] == "user-07"), None),
        "TCID": next((field["Values"][0]["value"] for field in entity["Fields"] if field["Name"] == "id"), None),
        "Component": next((field["Values"][0]["value"] for field in entity["Fields"] if field["Name"] == "user-02"), None),
        "Apllication": next((field["Values"][0]["value"] for field in entity["Fields"] if field["Name"] == "user-10"), None),
        "Release": next((field["Values"][0]["value"] for field in entity["Fields"] if field["Name"] == "user-04"), None)
    }
    for entity in data["entities"]
]

# Print the final output
print(final_output)

import pandas as pd

# Define the input data
input1 = [
    {"last_modified": "2024-11-14 02:41:20", "name": "HKMA Remarks 1_IR STD_InterestRateCrossCurr", "config_id": "1001", "parent_id": "1"},
    {"last_modified": "2024-11-14 02:41:20", "name": "HKMA Remarks 1_IR", "config_id": "1002", "parent_id": "2"}
]

input2 = [
    {'JIRA': 'JFSA-07', 'TCID': '1', 'Component': 'JFSA-02', 'Apllication': 'JFSA-10', 'Release': 'JFSA-04'},
    {'JIRA': '07', 'TCID': '2', 'Component': '02', 'Apllication': '10', 'Release': '04'}
]

# Convert input1 and input2 into DataFrames
df_input1 = pd.DataFrame(input1)
df_input2 = pd.DataFrame(input2)

# Join on parent_id from df_input1 and TCID from df_input2
result = pd.merge(df_input1, df_input2, left_on='parent_id', right_on='TCID', how='inner')

# Drop the parent_id column from the result
result = result.drop(columns=['parent_id'])

# Convert the result to JSON format
json_result = result[['JIRA', 'TCID', 'Component', 'Apllication', 'Release']].to_json(orient='records')

# Print the JSON result
print(json_result)
