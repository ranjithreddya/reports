db table:
col1,col2,col3,col4,col5
1,lkl,lkl,lkl,lkl
2,fff,fff,fff,fff
3,ffefer,ffefer,ffefer,ffefer
4,ffefer,ffefer,ffefer,ffefer
5,rfw,rfw,rfw,rfw




input csv:
col1,col2,col3,col4,col5
1,lkl,lkl,lkl,lkl
3,fff,fff,fff,fff
3,ffefer,ffefer,ffefer,ffefer
6,ffefer,ffefer,ffefer,ffefer
7,rfw,rfw,rfw,rfw


i have input table need to bulk update or create in db table using django api and uniqidentier is col1 if col1 value is not there need bulk create or bulk update


########################################################################################################################################

from django.db import models, IntegrityError

# Assuming your model looks something like this
class YourModel(models.Model):
    col1 = models.IntegerField(unique=True)
    col2 = models.CharField(max_length=255)
    col3 = models.CharField(max_length=255)
    col4 = models.CharField(max_length=255)
    col5 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.col1} - {self.col2}"

def bulk_update_or_create(input_data):
    """
    Bulk update or create records based on the unique identifier `col1`.
    """
    if not input_data:
        return
    
    # Extract the `col1` values from the input data for faster lookup
    col1_values = [row['col1'] for row in input_data]
    
    # Fetch the existing records in a single query to avoid multiple DB hits
    existing_records = YourModel.objects.filter(col1__in=col1_values)
    
    # Create a dictionary of existing records indexed by col1 for fast lookup
    existing_dict = {record.col1: record for record in existing_records}
    
    # Prepare lists for bulk updates and creates
    update_records = []
    create_records = []

    # Iterate over the input data
    for row in input_data:
        col1_value = row['col1']
        # If the record exists, update it directly
        if col1_value in existing_dict:
            record = existing_dict[col1_value]
            record.col2 = row['col2']
            record.col3 = row['col3']
            record.col4 = row['col4']
            record.col5 = row['col5']
            update_records.append(record)
        else:
            # If the record doesn't exist, create it
            create_records.append(YourModel(
                col1=col1_value,
                col2=row['col2'],
                col3=row['col3'],
                col4=row['col4'],
                col5=row['col5']
            ))

    # Perform bulk updates if any records were updated
    if update_records:
        try:
            YourModel.objects.bulk_update(update_records, ['col2', 'col3', 'col4', 'col5'])
        except IntegrityError as e:
            print(f"Error updating records: {e}")
            # Optionally, log or raise the error depending on your needs

    # Perform bulk creation if any records were new
    if create_records:
        try:
            YourModel.objects.bulk_create(create_records)
        except IntegrityError as e:
            print(f"Error creating records: {e}")
            # Optionally, log or raise the error depending on your needs

# Example input data (CSV data as a list of dictionaries)
input_data = [
    {'col1': 1, 'col2': 'lkl', 'col3': 'lkl', 'col4': 'lkl', 'col5': 'lkl'},
    {'col1': 3, 'col2': 'fff', 'col3': 'fff', 'col4': 'fff', 'col5': 'fff'},
    {'col1': 3, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 6, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 7, 'col2': 'rfw', 'col3': 'rfw', 'col4': 'rfw', 'col5': 'rfw'}
]

# Call the bulk update/create function
bulk_update_or_create(input_data)


##################################################################################################################################

class YourModel:
    def __init__(self, col1, col2, col3, col4, col5):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4
        self.col5 = col5

    def __repr__(self):
        return f"YourModel(col1={self.col1}, col2={self.col2}, col3={self.col3}, col4={self.col4}, col5={self.col5})"


def bulk_update_or_create(input_data, existing_data):
    """
    Simulate bulk update or create based on `col1` as unique identifier.
    input_data: List of dictionaries representing new data.
    existing_data: List of `YourModel` objects simulating existing database records.
    """

    # Convert existing records into a dictionary with col1 as key for fast lookup
    existing_dict = {record.col1: record for record in existing_data}

    # Prepare lists for updates and creates
    update_records = []
    create_records = []

    for row in input_data:
        col1_value = row['col1']

        if col1_value in existing_dict:
            # If record exists, update it
            record = existing_dict[col1_value]
            record.col2 = row['col2']
            record.col3 = row['col3']
            record.col4 = row['col4']
            record.col5 = row['col5']
            update_records.append(record)
        else:
            # If record doesn't exist, create it
            create_records.append(YourModel(
                col1=col1_value,
                col2=row['col2'],
                col3=row['col3'],
                col4=row['col4'],
                col5=row['col5']
            ))

    # Update the `existing_data` list with the modified records
    for updated_record in update_records:
        # Find the index of the record to update
        for i, record in enumerate(existing_data):
            if record.col1 == updated_record.col1:
                existing_data[i] = updated_record  # Replace the old record with the updated one

    # Print the records that would be updated and created
    print(f"Updating the following records:")
    for record in update_records:
        print(record)

    print(f"Creating the following records:")
    for record in create_records:
        print(record)

    # Return updated and created records
    return update_records, create_records


# Simulate existing records (this would represent your database records)
existing_data = [
    YourModel(1, 'lkl', 'lkl', 'lkl', 'lkl'),
    YourModel(2, 'fff', 'fff', 'fff', 'fff'),
    YourModel(3, 'ffefer', 'ffefer', 'ffefer', 'ffefer'),
    YourModel(4, 'rfw', 'rfw', 'rfw', 'rfw')
]

# Input data simulating the CSV input
input_data = [
    {'col1': 1, 'col2': 'lkl', 'col3': 'lkl', 'col4': 'lkl', 'col5': 'lkl'},   # No change
    {'col1': 3, 'col2': 'fff', 'col3': 'fff', 'col4': 'fff', 'col5': 'fff'},   # Update
    {'col1': 3, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'f'},  # No change
    {'col1': 6, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},  # Create
    {'col1': 7, 'col2': 'rfw', 'col3': 'rfw', 'col4': 'rfw', 'col5': 'rfw'}   # Create
]

# Call the function to simulate the update/create process
update_records, create_records = bulk_update_or_create(input_data, existing_data)

# Final state of the "database" (existing_data after updates)
print("\nFinal existing records after updates:")
for record in existing_data:
    print(record)

# Final state of the "database" (new records created)
print("\nNew records created:")
for record in create_records:
    print(record)



##########################################################################################################################

import snowflake.connector
from snowflake.connector.errors import ProgrammingError
from typing import List, Dict

# Snowflake connection setup
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='<your_user>',
        password='<your_password>',
        account='<your_account>',
        warehouse='<your_warehouse>',
        database='<your_database>',
        schema='<your_schema>',
    )

# Function to bulk update or create records in Snowflake
def bulk_update_or_create(input_data: List[Dict]):
    if not input_data:
        return
    
    # Extract the `col1` values from the input data for faster lookup
    col1_values = [row['col1'] for row in input_data]
    
    # Convert the list of col1 values to a string for the SQL query
    col1_values_str = ','.join(map(str, col1_values))

    # Establish a Snowflake connection
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        # Step 1: Fetch existing records from Snowflake based on `col1`
        query = f"""
        SELECT col1 FROM your_table WHERE col1 IN ({col1_values_str})
        """
        cursor.execute(query)
        existing_records = cursor.fetchall()
        existing_col1_values = {record[0] for record in existing_records}

        # Prepare for bulk insert and update
        update_records = []
        create_records = []

        # Step 2: Iterate through the input data and determine if it's an update or create
        for row in input_data:
            col1_value = row['col1']
            if col1_value in existing_col1_values:
                # Record exists, prepare for update
                update_query = f"""
                UPDATE your_table 
                SET col2 = '{row['col2']}', col3 = '{row['col3']}', col4 = '{row['col4']}', col5 = '{row['col5']}'
                WHERE col1 = {col1_value}
                """
                update_records.append(update_query)
            else:
                # Record doesn't exist, prepare for insert
                create_query = f"""
                INSERT INTO your_table (col1, col2, col3, col4, col5)
                VALUES ({col1_value}, '{row['col2']}', '{row['col3']}', '{row['col4']}', '{row['col5']}')
                """
                create_records.append(create_query)

        # Step 3: Execute bulk update queries if any updates were found
        if update_records:
            for update_query in update_records:
                try:
                    cursor.execute(update_query)
                except ProgrammingError as e:
                    print(f"Error updating record for col1={col1_value}: {e}")
                    # Handle error (e.g., log, continue, or raise)

        # Step 4: Execute bulk insert queries if any new records were found
        if create_records:
            for create_query in create_records:
                try:
                    cursor.execute(create_query)
                except ProgrammingError as e:
                    print(f"Error creating record for col1={col1_value}: {e}")
                    # Handle error (e.g., log, continue, or raise)

    finally:
        cursor.close()
        conn.close()

# Example input data (CSV data as a list of dictionaries)
input_data = [
    {'col1': 1, 'col2': 'lkl', 'col3': 'lkl', 'col4': 'lkl', 'col5': 'lkl'},
    {'col1': 3, 'col2': 'fff', 'col3': 'fff', 'col4': 'fff', 'col5': 'fff'},
    {'col1': 3, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 6, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 7, 'col2': 'rfw', 'col3': 'rfw', 'col4': 'rfw', 'col5': 'rfw'}
]

# Call the bulk update/create function
bulk_update_or_create(input_data)



#################################################################################################################################

import snowflake.connector
from snowflake.connector.errors import ProgrammingError
from typing import List, Dict

# Snowflake connection setup
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='<your_user>',
        password='<your_password>',
        account='<your_account>',
        warehouse='<your_warehouse>',
        database='<your_database>',
        schema='<your_schema>',
    )

# Function to bulk update or create records in Snowflake using MERGE
def bulk_update_or_create(input_data: List[Dict]):
    if not input_data:
        return
    
    # Establish a Snowflake connection
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        # Step 1: Create a temporary table to load the input data
        cursor.execute("""
        CREATE OR REPLACE TEMPORARY TABLE temp_table (
            col1 INT,
            col2 STRING,
            col3 STRING,
            col4 STRING,
            col5 STRING
        )
        """)

        # Step 2: Prepare the input data for bulk insert into the temporary table
        insert_values = []
        for row in input_data:
            insert_values.append(f"({row['col1']}, '{row['col2']}', '{row['col3']}', '{row['col4']}', '{row['col5']}')")

        # Step 3: Bulk insert into the temporary table
        if insert_values:
            insert_query = f"""
            INSERT INTO temp_table (col1, col2, col3, col4, col5) 
            VALUES {', '.join(insert_values)}
            """
            cursor.execute(insert_query)

        # Step 4: Perform the MERGE operation (upsert) using the temporary table
        merge_query = """
        MERGE INTO your_table AS target
        USING temp_table AS source
        ON target.col1 = source.col1
        WHEN MATCHED THEN
            UPDATE SET
                target.col2 = source.col2,
                target.col3 = source.col3,
                target.col4 = source.col4,
                target.col5 = source.col5
        WHEN NOT MATCHED THEN
            INSERT (col1, col2, col3, col4, col5)
            VALUES (source.col1, source.col2, source.col3, source.col4, source.col5)
        """
        cursor.execute(merge_query)
        
        # Step 5: Drop the temporary table explicitly after the operation
        cursor.execute("DROP TABLE IF EXISTS temp_table")
        
    except ProgrammingError as e:
        print(f"Error executing bulk update/create: {e}")
        # Handle error (e.g., log, continue, or raise)
        
    finally:
        cursor.close()
        conn.close()

# Example input data (CSV data as a list of dictionaries)
input_data = [
    {'col1': 1, 'col2': 'lkl', 'col3': 'lkl', 'col4': 'lkl', 'col5': 'lkl'},
    {'col1': 3, 'col2': 'fff', 'col3': 'fff', 'col4': 'fff', 'col5': 'fff'},
    {'col1': 3, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 6, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 7, 'col2': 'rfw', 'col3': 'rfw', 'col4': 'rfw', 'col5': 'rfw'}
]

# Call the bulk update/create function
bulk_update_or_create(input_data)



##################################################################################################################

import snowflake.connector  # Importing the Snowflake connector to interact with Snowflake
from snowflake.connector.errors import ProgrammingError  # Importing error class for handling programming errors in SQL
from typing import List, Dict  # Importing types for type hinting (List of Dicts)

# Function to establish a Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='<your_user>',  # Replace with your Snowflake username
        password='<your_password>',  # Replace with your Snowflake password
        account='<your_account>',  # Replace with your Snowflake account URL
        warehouse='<your_warehouse>',  # Replace with your Snowflake warehouse
        database='<your_database>',  # Replace with the name of your Snowflake database
        schema='<your_schema>',  # Replace with the name of your Snowflake schema
    )

# Main function to bulk update or insert records into Snowflake
def bulk_update_or_create(input_data: List[Dict]):
    if not input_data:  # If the input data is empty, exit the function early
        return
    
    # Establish a connection to Snowflake
    conn = get_snowflake_connection()
    cursor = conn.cursor()  # Create a cursor to interact with Snowflake

    try:
        # Step 1: Create a temporary table to hold the input data
        cursor.execute("""
        CREATE OR REPLACE TEMPORARY TABLE temp_table (
            col1 INT,  # Column 1: Integer type for primary key or unique identifier
            col2 STRING,  # Column 2: String type
            col3 STRING,  # Column 3: String type
            col4 STRING,  # Column 4: String type
            col5 STRING   # Column 5: String type
        )
        """)

        # Step 2: Prepare the input data for bulk insert
        insert_values = []  # Initialize an empty list to hold formatted insert values
        for row in input_data:  # Loop through each row in the input data
            # Format each row into SQL-friendly values for insertion into the temp table
            insert_values.append(f"({row['col1']}, '{row['col2']}', '{row['col3']}', '{row['col4']}', '{row['col5']}')")

        # Step 3: Bulk insert into the temporary table
        if insert_values:  # Check if there are any values to insert
            # Create the full SQL insert query by joining the formatted rows with commas
            insert_query = f"""
            INSERT INTO temp_table (col1, col2, col3, col4, col5) 
            VALUES {', '.join(insert_values)}
            """
            cursor.execute(insert_query)  # Execute the insert query to load data into the temp table

        # Step 4: Perform the MERGE operation (upsert) between the temp table and target table
        merge_query = """
        MERGE INTO your_table AS target  # Target table in your database (replace with your actual table name)
        USING temp_table AS source  # Source is the temporary table
        ON target.col1 = source.col1  # Match records based on 'col1'
        WHEN MATCHED THEN  # If the records match, update the target table
            UPDATE SET
                target.col2 = source.col2,  # Update 'col2' with data from the temp table
                target.col3 = source.col3,  # Update 'col3'
                target.col4 = source.col4,  # Update 'col4'
                target.col5 = source.col5   # Update 'col5'
        WHEN NOT MATCHED THEN  # If no match is found, insert new records into the target table
            INSERT (col1, col2, col3, col4, col5)
            VALUES (source.col1, source.col2, source.col3, source.col4, source.col5)
        """
        cursor.execute(merge_query)  # Execute the MERGE query to perform the upsert

        # Step 5: Drop the temporary table after the operation
        cursor.execute("DROP TABLE IF EXISTS temp_table")  # Drop the temporary table to clean up

    except ProgrammingError as e:  # Catch any errors related to SQL execution
        print(f"Error executing bulk update/create: {e}")  # Print the error message
        # You can log the error or take further actions here (e.g., retrying or raising the exception)
    
    finally:
        # Ensure that the cursor and connection are closed regardless of success or failure
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection to Snowflake

# Example input data (list of dictionaries, each representing a row of data)
input_data = [
    {'col1': 1, 'col2': 'lkl', 'col3': 'lkl', 'col4': 'lkl', 'col5': 'lkl'},
    {'col1': 3, 'col2': 'fff', 'col3': 'fff', 'col4': 'fff', 'col5': 'fff'},
    {'col1': 3, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 6, 'col2': 'ffefer', 'col3': 'ffefer', 'col4': 'ffefer', 'col5': 'ffefer'},
    {'col1': 7, 'col2': 'rfw', 'col3': 'rfw', 'col4': 'rfw', 'col5': 'rfw'}
]

# Call the function to perform the bulk update/create operation with the input data
bulk_update_or_create(input_data)

