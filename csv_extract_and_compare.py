import pandas as pd

# Provided data
csv1 = pd.DataFrame({
    'c1': [123, 456],
    'c2': ['a', 'b'],
    'c3': ['a1', 'b2']
})

csv2 = pd.DataFrame({
    'd1': [123, 456 ],
    'd22': ['a', 'b'],
    'd3': [0, 0],
    'd4': ['y', 'n'],
    'd5': ['n', 'y']
})

# Define the common key pairs
common_keys_csv1 = ['c1', 'c2']
common_keys_csv2 = ['d1', 'd22']

# Perform the merge operation
merged_df = pd.merge(csv1, csv2, left_on=common_keys_csv1, right_on=common_keys_csv2)

# Select all columns from csv2
csv2_columns = csv2.columns.tolist()
output_df = merged_df[csv2_columns]

# Display the output DataFrame
print(output_df)




# import pandas as pd
# import numpy as np

# # Sample CSV data
# data_csv1 = {
#     'c1': [123, 456],
#     'c2': ['y', 'n'],
#     'c3': ['n', 'n']
# }

# data_csv3 = {
#     'c1': [123, 789],
#     'c2': ['y', 'y'],
#     'c3': ['y', 'n']
# }

# # Create DataFrames
# df_csv1 = pd.DataFrame(data_csv1)
# df_csv3 = pd.DataFrame(data_csv3)

# # Perform a full outer join on 'c1'
# df_merged = pd.merge(df_csv1, df_csv3, on='c1', how='outer', suffixes=('_csv1', '_csv2'))

# # Initialize result list
# result = []

# # Compare columns c2 and c3
# for _, row in df_merged.iterrows():
#     for column in ['c2', 'c3']:
#         csv1_value = row[f'{column}_csv1'] if pd.notna(row[f'{column}_csv1']) else None
#         csv2_value = row[f'{column}_csv2'] if pd.notna(row[f'{column}_csv2']) else None
#         test_result = 'pass' if csv1_value == csv2_value else 'fail'
#         result.append({
#             'column': column,
#             'csv1_value': csv1_value,
#             'csv2_value': csv2_value,
#             'test_resul': test_result,
#             'uti': row['c1']
#         })

# # Print the result
# for item in result:
#     print(item)
