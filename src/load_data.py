import pandas as pd
import os

def load_data(file_path):
    """
    Loads a dataset from a CSV or Excel file.
    
    Args:
        file_path (str): Path to the dataset file.
        
    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load CSV file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    
    # Load Excel file
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")
    
    print(f"Data loaded successfully! Shape: {df.shape}")
    return df

# Test the function (modify with your actual file path)
if __name__ == "__main__":
    data_path = "../data/UHI Data.xlsx" # Change this to your actual dataset file
    df = load_data(data_path)
    print(df.head())  # Display first 5 rows
