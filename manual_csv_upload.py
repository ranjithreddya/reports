import pandas as pd
from io import StringIO

# Simulate the CSV input as a string
csv_data = """col1,col2,col3
test1,set1,ts1
test2,set2,ts2
test3,set3,ts3"""


csv_file = StringIO(csv_data)


df = pd.read_csv(csv_file)


df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'


columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]


table_name = 'temp_csv_data'


create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {table_name} AS\nSELECT "

# Dynamically add the columns in the SELECT statement
select_columns = [f"'{col}' AS {col}" for col in df.columns]
create_table_sql += ",\n".join(select_columns) + "\n"

# Step 2: Dynamically create the values in the SELECT statement (one row for each row in the DataFrame)
select_values = []
for _, row in df.iterrows():
    values = [f"'{row[col]}'" for col in df.columns]  # Escape each value with single quotes
    select_values.append(f"({', '.join(values)})")

# Combine the SELECT values into a single SQL statement
create_table_sql += f"FROM VALUES\n" + ",\n".join(select_values) + ";"

# Print the generated SQL query
print(create_table_sql)

CREATE OR REPLACE TEMPORARY TABLE temp_csv_data (
    file STRING,
    type STRING,
    col1 STRING,
    col2 STRING,
    col3 STRING
);

INSERT INTO temp_csv_data (file, type, col1, col2, col3)
SELECT
    '/apps/dpo/text.csv' AS file,
    'csv' AS type,
    'test1' AS col1,
    'set1' AS col2,
    'ts1' AS col3
UNION ALL
SELECT
    '/apps/dpo/text.csv' AS file,
    'csv' AS type,
    'test2' AS col1,
    'set2' AS col2,
    'ts2' AS col3
UNION ALL
SELECT
    '/apps/dpo/text.csv' AS file,
    'csv' AS type,
    'test3' AS col1,
    'set3' AS col2,
    'ts3' AS col3;



    import pandas as pd
from io import StringIO

# Simulate the CSV input as a string
csv_data = """col1,col2,col3
test1,set1,ts1
test2,set2,ts2
test3,set3,ts3"""

# Use StringIO to treat the string as a file-like object
csv_file = StringIO(csv_data)

# Read the CSV from the string
df = pd.read_csv(csv_file)

# Add the extra columns
df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'

# Reorder columns to move 'file' and 'type' to the front
columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]

# Print the DataFrame for reference
print(df)

# Now, we will generate a Snowflake SQL query for CREATE and INSERT at the same time
table_name = 'temp_csv_data'

# Step 1: Create the CREATE TABLE statement dynamically based on the DataFrame columns
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {table_name} (\n"

# Dynamically create the column definitions for the CREATE statement
for col in df.columns:
    create_table_sql += f"    {col} STRING,\n"

# Remove the trailing comma and newline from the last column definition
create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

# Step 2: Dynamically create the INSERT INTO statement with SELECT values
insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)})\nSELECT "

# Dynamically add the row values as part of the SELECT statement
select_values = []
for _, row in df.iterrows():
    # Create dynamic value list for each row, properly quoted
    values = [f"'{row[col]}'" for col in df.columns]  # Escape each value with single quotes
    select_values.append(f"({', '.join(values)})")

# Combine the SELECT values into a single SQL statement
insert_sql += ",\n".join(select_values) + ";"

# Combine the CREATE and INSERT SQL statements
full_sql = create_table_sql + "\n" + insert_sql

# Print the generated SQL query
print(full_sql)


import snowflake.connector

# Establish connection to Snowflake
conn = snowflake.connector.connect(
    user='<your_user>',
    password='<your_password>',
    account='<your_account>',
    warehouse='<your_warehouse>',
    database='<your_database>',
    schema='<your_schema>'
)

# Function to generate and execute the dynamic SQL
def execute_merge():
    try:
        # Create a cursor object
        cur = conn.cursor()

        # Get the list of columns for the temp_table (assuming temp_table has the same columns as main_table)
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'TEMP_TABLE' AND table_schema = 'YOUR_SCHEMA'
            ORDER BY ordinal_position;
        """)

        # Fetch column names from the temp_table
        temp_table_columns = [row[0] for row in cur.fetchall()]

        # Ensure both tables have columns that need to be handled in the merge
        # Build the column list for the INSERT and UPDATE statements
        column_list = ", ".join(temp_table_columns)
        set_clause = ", ".join([f"target.{col} = source.{col}" for col in temp_table_columns])
        values_clause = ", ".join([f"source.{col}" for col in temp_table_columns])

        # Build the dynamic MERGE statement
        merge_sql = f"""
            MERGE INTO main_table AS target
            USING temp_table AS source
            ON target.id = source.id  -- Matching condition
            WHEN MATCHED THEN
                UPDATE SET {set_clause}
            WHEN NOT MATCHED THEN
                INSERT ({column_list}) 
                VALUES ({values_clause});
        """

        # Print the dynamic SQL for debugging purposes
        print("Generated MERGE SQL:\n", merge_sql)

        # Execute the MERGE statement
        cur.execute(merge_sql)
        
        print("MERGE statement executed successfully!")

    except Exception as e:
        print(f"Error executing the MERGE statement: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

# Call the function to execute the merge
execute_merge()



import pandas as pd

# Load CSV
df = pd.read_csv(csv_file)

# Add extra columns
df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'

# Reorder columns to move 'file' and 'type' to the front
columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]

# Print the DataFrame for reference
print(df)

# Now, we will generate a Snowflake SQL query for CREATE and INSERT at the same time
table_name = 'temp_csv_data'

# Step 1: Dynamically create the CREATE TABLE statement based on the DataFrame columns and data types
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {table_name} (\n"

# Infer data types and add column definitions to the CREATE statement
for col in df.columns:
    # Check if the column contains non-string data and use a more specific type
    if df[col].dtype == 'int64':
        data_type = 'INT'
    elif df[col].dtype == 'float64':
        data_type = 'FLOAT'
    elif df[col].dtype == 'datetime64[ns]':
        data_type = 'DATE'
    else:
        data_type = 'STRING'
    
    # Handle columns with spaces or hyphens
    if ' ' in col or '-' in col:
        create_table_sql += f'    "{col}" {data_type},\n'
    else:
        create_table_sql += f'    {col} {data_type},\n'

# Remove the trailing comma and newline from the last column definition
create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

# Step 2: Create the INSERT INTO statement dynamically
columns = ', '.join([f'"{col}"' if ' ' in col or '-' in col else col for col in df.columns])
insert_sql = f"INSERT INTO {table_name} ({columns})\nSELECT "

select_values = []
for _, row in df.iterrows():
    # Create dynamic value list for each row, properly quoted
    values = [f"'{row[col]}'" if pd.notnull(row[col]) else 'NULL' for col in df.columns]
    select_values.append(f"({', '.join(values)})")

insert_sql += ",\n".join(select_values) + ";"

# Execute SQL statements (assuming you have a cursor object for database interaction)
cursor.execute(create_table_sql)
cursor.execute(insert_sql)


merge_sql = f"""
    MERGE INTO main_table AS target
    USING temp_table AS source
    ON target.id = source.id  -- Matching condition
    WHEN MATCHED THEN
        UPDATE SET 
            {', '.join([f"target.{col} = CAST(source.{col} AS {target_type})" for col, target_type in zip(column_list.split(','), target_column_types)])
        }
    WHEN NOT MATCHED THEN
        INSERT ({column_list}) 
        VALUES (
            {', '.join([f"CAST(source.{col} AS {target_type})" for col, target_type in zip(column_list.split(','), target_column_types)])}
        );
"""


##################################################

import pandas as pd

# Read the CSV into a DataFrame
df = pd.read_csv(csv_file)

# Add the 'file' and 'type' columns
df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'

# Reorder the columns to have 'file' and 'type' at the beginning
columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]

# Initialize the CREATE TABLE SQL statement
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE temp_csv_data (\n"

# Function to detect appropriate data types
def detect_data_type(col_data):
    # Try to parse as date first
    try:
        pd.to_datetime(col_data, errors='raise')  # Try converting to datetime
        return 'TIMESTAMP'  # Use TIMESTAMP for date-time columns
    except Exception:
        pass

    # Check if the column can be cast to numeric
    if pd.to_numeric(col_data, errors='coerce').notna().all():
        if col_data.dtype == 'float64':
            return 'FLOAT'
        return 'INT'

    # Default to STRING if not a date or numeric type
    return 'STRING'

# Loop through the columns of the DataFrame and assign appropriate data types
for col in df.columns:
    # Detect the data type dynamically
    data_type = detect_data_type(df[col])

    # Add column to the CREATE TABLE SQL, ensuring columns with spaces or dashes are quoted
    if ' ' in col or '-' in col:
        create_table_sql += f'    "{col}" {data_type},\n'
    else:
        create_table_sql += f'    {col} {data_type},\n'

# Remove the trailing comma and add closing parentheses
create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

# Now create the INSERT INTO statement
columns = ', '.join([f'"{col}"' if ' ' in col or '-' in col else col for col in df.columns])
insert_sql = f"INSERT INTO {table_name} ({columns})\nSELECT "

# Prepare the VALUES part of the INSERT statement
select_values = []
for _, row in df.iterrows():
    # Create dynamic value list for each row, properly quoted
    values = [f"'{row[col]}'" if pd.notnull(row[col]) else 'NULL' for col in df.columns]
    select_values.append(f"({', '.join(values)})")

# Append the values to the insert SQL
insert_sql += ",\n".join(select_values) + ";"

# Execute the SQL to create the table and insert the data
cursor.execute(create_table_sql)
cursor.execute(insert_sql)




import pandas as pd

# Read the CSV into a DataFrame
df = pd.read_csv(csv_file)

# Add the 'file' and 'type' columns
df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'

# Reorder the columns to have 'file' and 'type' at the beginning
columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]

# Initialize the CREATE TABLE SQL statement
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE temp_csv_data (\n"

# Function to detect appropriate data types
def detect_data_type(col_name, col_data):
    # Check if the column can be interpreted as a date
    try:
        pd.to_datetime(col_data, errors='raise')  # Try converting to datetime
        return "TIMESTAMP_NTZ(9)"  # Use TIMESTAMP for date-time columns
    except Exception:
        pass

    # Check if the column can be cast to numeric (either integer or float)
    numeric_data = pd.to_numeric(col_data, errors='coerce')
    if numeric_data.notna().all():
        # If it's float data, we assign FLOAT; otherwise, NUMBER
        return "FLOAT" if col_data.dtype == 'float64' else "NUMBER(38,0)"
    
    # Check for boolean columns (only two unique values)
    if col_data.nunique() == 2 and col_data.dropna().isin([True, False]).all():
        return "BOOLEAN"

    # Default to VARCHAR(16777216) if not a date, numeric, or boolean
    return "VARCHAR(16777216)"

# Loop through the columns of the DataFrame and assign appropriate data types
for col in df.columns:
    # Detect the data type dynamically based on the column name and values
    data_type = detect_data_type(col, df[col])

    # Add column to the CREATE TABLE SQL, ensuring columns with spaces or dashes are quoted
    if ' ' in col or '-' in col:
        create_table_sql += f'    "{col}" {data_type},\n'
    else:
        create_table_sql += f'    {col} {data_type},\n'

# Remove the trailing comma and add closing parentheses
create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

# Now create the INSERT INTO statement
columns = ', '.join([f'"{col}"' if ' ' in col or '-' in col else col for col in df.columns])
insert_sql = f"INSERT INTO {table_name} ({columns})\nSELECT "

# Prepare the VALUES part of the INSERT statement
select_values = []
for _, row in df.iterrows():
    # Create dynamic value list for each row, properly quoted
    values = [f"'{row[col]}'" if pd.notnull(row[col]) else 'NULL' for col in df.columns]
    select_values.append(f"({', '.join(values)})")

# Append the values to the insert SQL
insert_sql += ",\n".join(select_values) + ";"

# Execute the SQL to create the table and insert the data
cursor.execute(create_table_sql)
cursor.execute(insert_sql)




import pandas as pd

# Read the CSV into a DataFrame
df = pd.read_csv(csv_file)

# Add the 'file' and 'type' columns
df['file'] = '/apps/dpo/text.csv'
df['type'] = 'csv'

# Reorder the columns to have 'file' and 'type' at the beginning
columns = ['file', 'type'] + [col for col in df.columns if col not in ['file', 'type']]
df = df[columns]

# Initialize the CREATE TABLE SQL statement
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE temp_csv_data (\n"

# Function to detect appropriate data types
def detect_data_type(col_name, col_data):
    # Check if the column can be interpreted as a date
    try:
        pd.to_datetime(col_data, errors='raise')  # Try converting to datetime
        return "TIMESTAMP_NTZ(9)"  # Use TIMESTAMP for date-time columns
    except Exception:
        pass

    # Check if the column can be cast to numeric (either integer or float)
    numeric_data = pd.to_numeric(col_data, errors='coerce')
    if numeric_data.notna().all():
        # If it's float data, we assign FLOAT; otherwise, NUMBER
        return "FLOAT" if col_data.dtype == 'float64' else "NUMBER(38,0)"
    
    # Check for boolean columns (only two unique values)
    # First, handle cases where boolean values are represented as strings ("True", "False")
    if col_data.dropna().isin(['True', 'False']).all():
        return "BOOLEAN"
    
    # Check for actual boolean columns (True, False)
    if col_data.dropna().isin([True, False]).all():
        return "BOOLEAN"

    # Default to VARCHAR(16777216) if not a date, numeric, or boolean
    return "VARCHAR(16777216)"

# Loop through the columns of the DataFrame and assign appropriate data types
for col in df.columns:
    # Detect the data type dynamically based on the column name and values
    data_type = detect_data_type(col, df[col])

    # Add column to the CREATE TABLE SQL, ensuring columns with spaces or dashes are quoted
    if ' ' in col or '-' in col:
        create_table_sql += f'    "{col}" {data_type},\n'
    else:
        create_table_sql += f'    {col} {data_type},\n'

# Remove the trailing comma and add closing parentheses
create_table_sql = create_table_sql.rstrip(',\n') + "\n);"

# Now create the INSERT INTO statement
columns = ', '.join([f'"{col}"' if ' ' in col or '-' in col else col for col in df.columns])
insert_sql = f"INSERT INTO {table_name} ({columns})\nSELECT "

# Prepare the VALUES part of the INSERT statement
select_values = []
for _, row in df.iterrows():
    # Create dynamic value list for each row, properly quoted
    values = [f"'{row[col]}'" if pd.notnull(row[col]) else 'NULL' for col in df.columns]
    select_values.append(f"({', '.join(values)})")

# Append the values to the insert SQL
insert_sql += ",\n".join(select_values) + ";"

# Execute the SQL to create the table and insert the data
cursor.execute(create_table_sql)
cursor.execute(insert_sql)


##################################################################################

import pandas as pd

# Given list of dictionaries
data = [
    {'Column1': 'value1', 'Column2': 'value2', 'Column3': 'value3'},
    {'Column1': 'value4', 'Column2': 'value5', 'Column3': 'value6'},
    {'Column1': 'value7', 'Column2': 'value8', 'Column3': 'value9'}
]

# Convert list of dictionaries into a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)


import pandas as pd

# Example data for multiple iterations
data_sets = [
    [
        {'Column1': 'value1', 'Column2': 'value2', 'Column3': 'value3'},
        {'Column1': 'value4', 'Column2': 'value5', 'Column3': 'value6'}
    ],
    [
        {'Column1': 'value7', 'Column2': 'value8', 'Column3': 'value9'},
        {'Column1': 'value10', 'Column2': 'value11', 'Column3': 'value12'}
    ],
    [
        {'Column1': 'value13', 'Column2': 'value14', 'Column3': 'value15'},
        {'Column1': 'value16', 'Column2': 'value17', 'Column3': 'value18'}
    ]
]

# Create an empty list to collect DataFrames
dfs = []

# Loop through each data set, convert to DataFrame and append to list
for data in data_sets:
    df = pd.DataFrame(data)
    dfs.append(df)

# Concatenate all DataFrames in the list into one DataFrame
result_df = pd.concat(dfs, ignore_index=True)

# Display the resulting DataFrame
print(result_df)

