import os
import sys
import pandas as pd
from sklearn.impute import SimpleImputer
import pickle

# Ensure src is recognized as a module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.load_data import load_data
from src.preprocess import preprocess_data
from src.train_model import train_model
from src.predict import predict

# Define file paths
file_path = "data/UHI_Data.csv"
model_path = "models/model.pkl"

print("🔄 Loading dataset...")
data = load_data(file_path)

print("🔄 Preprocessing data...")
data = preprocess_data(data)

# Print available columns
print(f"✅ Available columns: {data.columns.tolist()}")

# Ensure 'UHI_Index' exists before proceeding
if "UHI_Index" not in data.columns:
    raise KeyError("❌ Column 'UHI_Index' not found! Check column names in dataset.")

# Prepare features (X) and target (y)
X = data.drop(columns=["UHI_Index", "datetime"], errors='ignore')
y = data["UHI_Index"]

# Handle missing values
if X.isnull().sum().sum() > 0:
    print("⚠️ Warning: Missing values detected. Imputing with median...")
    imputer = SimpleImputer(strategy="median")
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Load model & ensure features match
if os.path.exists(model_path):
    print("✅ Model already exists. Loading model...")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Ensure model is sklearn-based and features match
    if hasattr(model, "feature_names_in_"):
        trained_features = model.feature_names_in_
        missing_features = set(trained_features) - set(X.columns)
        extra_features = set(X.columns) - set(trained_features)

        if missing_features or extra_features:
            print(f"⚠️ Warning: Feature mismatch detected!\n"
                  f"   Missing in input: {missing_features}\n"
                  f"   Extra in input: {extra_features}")
            X = X[trained_features]  # Keep only the trained features
    else:
        print("⚠️ Warning: Model does not have 'feature_names_in_'. Ensure it's saved correctly.")
else:
    print("🔄 Training a new model...")
    train_model(X, y)

# Making a test prediction
print("🔄 Making a test prediction...")
sample_input = pd.DataFrame([X.iloc[0]], columns=X.columns)  # Wrap in DataFrame
predicted_value = predict(sample_input)

print(f"✅ Predicted UHI Index: {predicted_value}")
