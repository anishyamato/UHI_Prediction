import pandas as pd

def preprocess_data(df):
    """
    Preprocess the dataset by converting datetime, handling missing values, and ensuring correct data types.

    Args:
        df (pd.DataFrame): Raw data.

    Returns:
        pd.DataFrame: Preprocessed data.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("❌ Input data must be a pandas DataFrame.")

    # Ensure 'datetime' column exists
    if 'datetime' not in df.columns:
        raise KeyError("❌ Column 'datetime' not found in dataset. Check for typos.")

    # Convert 'datetime' column to a proper datetime format
    df['datetime'] = pd.to_datetime(df['datetime'], format="%d-%m-%Y %H:%M", errors='coerce')

    # Drop rows where datetime conversion failed
    df = df.dropna(subset=['datetime'])

    # Extract datetime features
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour

    # Convert numerical columns to appropriate types
    for col in ['Longitude', 'Latitude', 'UHI_Index']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop any rows where critical numerical columns failed to convert
    df = df.dropna(subset=['Longitude', 'Latitude', 'UHI_Index'])

    print(f"✅ Data preprocessing completed! Shape: {df.shape}")
    return df
