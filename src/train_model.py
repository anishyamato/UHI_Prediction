import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from src.load_data import load_data
from src.preprocess import preprocess_data

# Define file path & model path
DATA_PATH = "data/UHI_Data.csv"
MODEL_PATH = "models/model.pkl"

def train_model(X, y):
    """
    Train a machine learning model and save it.
    """
    print("🔄 Training the model...")

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Validate model
    y_pred = model.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    print(f"✅ Model trained successfully! MAE: {mae:.4f}")

    # Save the trained model
    save_model(model, MODEL_PATH)

def save_model(model, model_path):
    """
    Save the trained model using pickle.
    """
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Model saved at: {model_path}")

if __name__ == "__main__":
    print("🔄 Loading dataset...")
    data = load_data(DATA_PATH)
    data = preprocess_data(data)  # Preprocess dataset

    if "UHI_Index" in data.columns:
        X = data.drop(columns=["UHI_Index", "datetime"], errors='ignore')  
        y = data["UHI_Index"]
    else:
        raise KeyError("❌ Column 'UHI_Index' not found in dataset! Check column names.")

    train_model(X, y)  # Train the model
