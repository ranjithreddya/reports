import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL

# Step 1: Load your primary CSV data into pandas DataFrame
csv_file_path = '/apps/dpo/text.csv'  # Path to the primary CSV file
df = pd.read_csv(csv_file_path)
print("Primary data loaded into DataFrame:")
print(df.head())  # Display the first few rows for verification

# Step 2: Load extra data into pandas DataFrame (assuming 'extra_data.csv' or other data source)
extra_data = {
    'extra_col1': ['XYZ', 'XYZ'],
    'extra_col2': [1234, 1234],
    'extra_col3': ['AAA', 'AAA']
}
extra_df = pd.DataFrame(extra_data)
print("Extra data loaded into DataFrame:")
print(extra_df.head())  # Display the extra data for verification

# Step 3: Add the extra data to the left side (prepend it to the primary DataFrame)
# Ensure that the extra data has the same number of rows as the primary data
if len(extra_df) == 1:  # If the extra data has only one row, repeat it for all rows in the primary DataFrame
    extra_data_repeated = extra_df.iloc[0].to_frame().T  # Convert the first row to a DataFrame
    extra_df = pd.concat([extra_data_repeated] * len(df), ignore_index=True)  # Repeat it for all rows in primary data

# Now prepend the extra data columns to the left of the primary DataFrame
df = pd.concat([extra_df, df], axis=1)  # Axis=1 means we're concatenating along columns (left side)

# Verify the updated DataFrame
print("Updated DataFrame with extra data added to the left side:")
print(df.head())  # Check if the extra data has been added to the left

# Step 4: Set up Snowflake connection using SQLAlchemy
snowflake_connection = {
    'user': 'your_user',
    'password': 'your_password',
    'account': 'your_account',
    'warehouse': 'your_warehouse',
    'database': 'your_database',
    'schema': 'your_schema'
}

# Create a connection engine to Snowflake
engine = create_engine(
    URL(
        user=snowflake_connection['user'],
        password=snowflake_connection['password'],
        account=snowflake_connection['account'],
        warehouse=snowflake_connection['warehouse'],
        database=snowflake_connection['database'],
        schema=snowflake_connection['schema']
    )
)

# Step 5: Create a temporary table in Snowflake dynamically based on the DataFrame columns
temp_table_name = "TEMP_TABLE"

# Create table creation SQL based on the DataFrame columns and their data types
create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {temp_table_name} ("
for col, dtype in zip(df.columns, df.dtypes):
    # Map pandas data types to Snowflake data types
    if dtype == 'object':
        col_type = 'STRING'
    elif dtype == 'int64':
        col_type = 'NUMBER'
    elif dtype == 'float64':
        col_type = 'FLOAT'
    elif dtype == 'bool':
        col_type = 'BOOLEAN'
    else:
        col_type = 'STRING'  # Default type

    create_table_sql += f"{col} {col_type}, "

# Remove the trailing comma and close the parenthesis
create_table_sql = create_table_sql.rstrip(', ') + ')'

# Execute the SQL query to create the temporary table
with engine.connect() as conn:
    conn.execute(text(create_table_sql))

print(f"Temporary table '{temp_table_name}' created successfully.")

# Step 6: Insert the DataFrame data into the temporary table in Snowflake
df.to_sql(
    name=temp_table_name,
    con=engine,
    if_exists='append',  # Append to the temp table, not replace
    index=False
)

print(f"Data successfully uploaded to temporary table '{temp_table_name}'.")

# Step 7: Dynamically generate the MERGE INTO SQL statement

# Extract column names dynamically
columns = df.columns.tolist()
target_table = 'your_target_table'

# Construct the ON condition (e.g., matching on TxId_New_UnqTxIdr)
on_condition = " AND ".join([f"target.{col} = source.{col}" for col in columns if col != 'extra_col1' and col != 'extra_col2' and col != 'extra_col3'])

# Construct the UPDATE clause dynamically
update_clause = ", ".join([f"target.{col} = source.{col}" for col in columns if col != 'extra_col1' and col != 'extra_col2' and col != 'extra_col3'])

# Construct the INSERT clause dynamically
insert_clause = ", ".join(columns)
insert_values = ", ".join([f"source.{col}" for col in columns])

# Construct the complete MERGE SQL
merge_sql = f"""
MERGE INTO {target_table} AS target
USING {temp_table_name} AS source
ON {on_condition}
WHEN MATCHED THEN
    UPDATE SET
        {update_clause}
WHEN NOT MATCHED THEN
    INSERT ({insert_clause})
    VALUES ({insert_values});
"""

# Execute the MERGE SQL query
with engine.connect() as conn:
    conn.execute(text(merge_sql))

print(f"Data merged successfully into target table '{target_table}'.")

# Step 8: Clean up by dropping the temporary table (optional)
drop_temp_sql = f"DROP TABLE IF EXISTS {temp_table_name};"

with engine.connect() as conn:
    conn.execute(text(drop_temp_sql))

print(f"Temporary table '{temp_table_name}' dropped successfully.")
