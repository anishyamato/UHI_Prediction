import numpy as np
import pandas as pd
import joblib
import os

# Load the trained model
MODEL_PATH = "models/model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found at {MODEL_PATH}. Train the model first.")

model = joblib.load(MODEL_PATH)

def preprocess_input(input_data):
    """
    Preprocess input data for prediction by ensuring correct feature names and formats.

    Args:
        input_data (pd.DataFrame or list): Input data.

    Returns:
        pd.DataFrame: Processed data ready for prediction.
    """
    expected_features = ['Longitude', 'Latitude', 'year', 'month', 'day', 'hour']

    # Ensure input_data is a DataFrame
    if isinstance(input_data, list) or isinstance(input_data, np.ndarray):
        raise ValueError("❌ Input data should be a pandas DataFrame with correct columns.")

    # Convert datetime if present
    if 'datetime' in input_data.columns:
        input_data['datetime'] = pd.to_datetime(input_data['datetime'])
        input_data['year'] = input_data['datetime'].dt.year
        input_data['month'] = input_data['datetime'].dt.month
        input_data['day'] = input_data['datetime'].dt.day
        input_data['hour'] = input_data['datetime'].dt.hour
        input_data = input_data.drop(columns=['datetime'])

    # Ensure input data has expected features
    missing_features = [col for col in expected_features if col not in input_data.columns]
    if missing_features:
        raise ValueError(f"❌ Missing required features: {missing_features}")

    return input_data[expected_features]

def predict(input_data):
    """
    Predict the UHI Index for a given input sample.

    Args:
        input_data (pd.DataFrame): Input features for prediction.

    Returns:
        float: Predicted UHI Index.
    """
    processed_input = preprocess_input(input_data)
    prediction = model.predict(processed_input)
    return prediction[0]  # Return scalar value
