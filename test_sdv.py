import argparse
import pandas as pd
from sdv import GaussianCopula
from sdv.metadata import Metadata

# Function to select specified columns from the input DataFrame
def select_columns(df, selected_columns):
    # Ensure that the selected columns exist in the DataFrame
    available_columns = df.columns.tolist()
    selected_columns = [col for col in selected_columns if col in available_columns]
    
    # Raise an exception if any of the columns are not found in the CSV
    if not selected_columns:
        raise ValueError(f"No valid columns found from the selected columns: {selected_columns}")
    
    # Select the specified columns
    df_selected = df[selected_columns]
    return df_selected

# Function to detect column types dynamically for SDV
def get_column_types(df):
    metadata = Metadata()

    # Automatically infer column types
    for column in df.columns:
        dtype = df[column].dtype
        if dtype == 'object':
            metadata.add_column('user_data', column, sdtype='text')  # Treat object as text (VARCHAR)
        elif dtype == 'datetime64[ns]':
            metadata.add_column('user_data', column, sdtype='datetime')  # Datetime columns
        elif dtype == 'bool':
            metadata.add_column('user_data', column, sdtype='categorical')  # Treat boolean as categorical (ENUM)
        elif dtype in ['int64', 'float64']:
            metadata.add_column('user_data', column, sdtype='numeric')  # Numeric columns
        else:
            raise ValueError(f"Unsupported data type for column {column}: {dtype}")
    return metadata

# Main function to generate synthetic data
def generate_synthetic_data(csv_file, selected_columns, num_rows):
    # Load your input CSV
    df = pd.read_csv(csv_file)

    # Step 1: Select only the specified columns from the input DataFrame
    df_selected = select_columns(df, selected_columns)

    # Step 2: Define metadata for SDV based on the selected columns
    metadata = get_column_types(df_selected)

    # Step 3: Train the model
    model = GaussianCopula()
    model.fit(df_selected)

    # Step 4: Generate synthetic data based on the metadata, model, and number of rows
    synthetic_data = model.sample(num_rows=num_rows)

    # Step 5: Display or save the generated synthetic data
    print(synthetic_data.head())  # Display the synthetic data

    # Optionally, save to a new CSV
    synthetic_data.to_csv('synthetic_data.csv', index=False)

# Set up command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate synthetic data based on input CSV and selected columns.")
    parser.add_argument('csv_file', help="Path to the input CSV file")
    parser.add_argument('columns', help="Comma-separated list of columns to use (e.g., 'name,date_column,status')")
    parser.add_argument('num_rows', type=int, help="Number of rows to generate in the synthetic dataset")

    return parser.parse_args()

# Entry point of the script
if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()

    # Convert columns argument to a list of column names
    selected_columns = args.columns.split(',')

    # Generate synthetic data
    try:
        generate_synthetic_data(args.csv_file, selected_columns, args.num_rows)
    except Exception as e:
        print(f"Error: {e}")
