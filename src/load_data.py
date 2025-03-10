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
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    
    # Load dataset based on file type
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("❌ Unsupported file format. Please use CSV or Excel.")

        # Remove leading/trailing spaces in column names
        df.columns = df.columns.str.strip()

        print(f"✅ Data loaded successfully! Shape: {df.shape}")
        return df

    except Exception as e:
        raise RuntimeError(f"❌ Error while loading data: {e}")
