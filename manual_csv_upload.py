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


