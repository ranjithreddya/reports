import snowflake.connector

ctx = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account_identifier',
    warehouse='your_warehouse_name',
    database='your_database_name',
    schema='your_schema_name'
)

cs = ctx.cursor()
try:
    cs.execute("SELECT CURRENT_VERSION()")
    one_row = cs.fetchone()
    print(one_row)
finally:
    cs.close()
ctx.close()
