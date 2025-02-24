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
