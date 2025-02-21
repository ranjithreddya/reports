import pandas as pd
from sqlalchemy import create_engine, text
from snowflake.sqlalchemy import URL
import os

# Function to load multiple CSV files into a dictionary of DataFrames
def load_multiple_csvs(csv_paths):
    dataframes = {}
    for csv_path in csv_paths:
        table_name = os.path.basename(csv_path).replace(".csv", "")  # Use the file name (without extension) as table name
        df = pd.read_csv(csv_path)
        dataframes[table_name] = df
    return dataframes

# Step 1: Load multiple CSV files into DataFrames
csv_paths = ['/path/to/first.csv', '/path/to/second.csv', '/path/to/third.csv']  # List of CSV file paths
dataframes = load_multiple_csvs(csv_paths)

# Display the first few rows of each DataFrame to verify
for table_name, df in dataframes.items():
    print(f"DataFrame for table: {table_name}")
    print(df.head())

# Step 2: Add extra data or transform data corresponding to each CSV table
extra_data = {
    'extra_col1': ['XYZ'] * len(dataframes['first']),  # Adjust based on the size of each DataFrame
    'extra_col2': [1234] * len(dataframes['first']),
}

extra_df = pd.DataFrame(extra_data)

# Example: Process extra data per CSV file
for table_name, df in dataframes.items():
    # Dynamically add extra data for each table
    extra_data_for_table = extra_df.copy()
    df = pd.concat([extra_data_for_table] * len(df), axis=1)  # Prepend extra data columns
    dataframes[table_name] = df  # Update the DataFrame with extra data

# Step 3: Set up Snowflake connection using SQLAlchemy
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

# Step 4: Create a temporary table for each DataFrame and load data into Snowflake
for table_name, df in dataframes.items():
    temp_table_name = f"TEMP_{table_name}"

    # Create the table creation SQL based on the DataFrame columns and their data types
    create_table_sql = f"CREATE OR REPLACE TEMPORARY TABLE {temp_table_name} ("
    for col, dtype in zip(df.columns, df.dtypes):
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

    # Remove trailing comma and add closing parenthesis
    create_table_sql = create_table_sql.rstrip(', ') + ')'

    # Execute the table creation SQL in Snowflake
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
    
    print(f"Temporary table '{temp_table_name}' created successfully.")

    # Step 5: Insert the DataFrame data into the temporary table in Snowflake
    df.to_sql(
        name=temp_table_name,
        con=engine,
        if_exists='append',  # Append to the temp table
        index=False
    )

    print(f"Data for '{table_name}' uploaded to temporary table '{temp_table_name}'.")

    # Step 6: Generate MERGE INTO SQL for this table dynamically
    columns = df.columns.tolist()

    # Construct the ON condition (e.g., matching on TxId_New_UnqTxIdr)
    on_condition = " AND ".join([f"target.{col} = source.{col}" for col in columns])

    # Construct the UPDATE clause dynamically
    update_clause = ", ".join([f"target.{col} = source.{col}" for col in columns])

    # Construct the INSERT clause dynamically
    insert_clause = ", ".join(columns)
    insert_values = ", ".join([f"source.{col}" for col in columns])

    # Construct the complete MERGE SQL for the table
    merge_sql = f"""
    MERGE INTO {table_name} AS target
    USING {temp_table_name} AS source
    ON {on_condition}
    WHEN MATCHED THEN
        UPDATE SET
            {update_clause}
    WHEN NOT MATCHED THEN
        INSERT ({insert_clause})
        VALUES ({insert_values});
    """

    # Execute the MERGE SQL
    with engine.connect() as conn:
        conn.execute(text(merge_sql))
    
    print(f"Data successfully merged into target table '{table_name}'.")

    # Step 7: Clean up by dropping the temporary table (optional)
    drop_temp_sql = f"DROP TABLE IF EXISTS {temp_table_name};"

    with engine.connect() as conn:
        conn.execute(text(drop_temp_sql))
    
    print(f"Temporary table '{temp_table_name}' dropped successfully.")
