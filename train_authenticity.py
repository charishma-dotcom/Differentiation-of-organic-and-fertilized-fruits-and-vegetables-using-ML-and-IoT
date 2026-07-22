import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score

# 1. Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'fruit_authenticity_dataset.csv')

print(f"Loading dataset from: {csv_path}")

if not os.path.exists(csv_path):
    print(f"[ERROR] Could not find '{csv_path}'. Please run your dataset generator script first.")
    exit()

# 2. Load dataset
df = pd.read_csv(csv_path)

# 3. Feature Encoding
# We need to turn text data ('Apple', 'medium', 'vibrant') into numbers for Random Forest
label_encoders = {}
categorical_columns = ['item name', 'size', 'colour', 'shape']

print("Encoding categorical features...")
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le  # Store the encoder to reuse in your dashboard later

# Encode target label (organic -> 0, fertilized -> 1)
target_encoder = LabelEncoder()
df['status'] = target_encoder.fit_transform(df['status'])

# 4. Split Data into Features (X) and Target Label (y)
X = df[categorical_columns]
y = df['status']

# Split into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Feature Scaling
# Normalizes numerical bounds to optimize model stability
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Train Random Forest Classifier
print("\nTraining Random Forest Classifier on 20,000 records...")
# Using 100 decision trees inside the forest
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# 7. Evaluate Model Performance
y_pred = rf_model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*40)
print(f" Model Training Metrics (Accuracy: {accuracy:.2%})")
print("="*40)
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# 8. Export the Model Artifacts
# This overwrites your existing .pkl placeholders with the actual trained intelligence
model_path = os.path.join(BASE_DIR, 'authenticity_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'authenticity_scaler.pkl')
features_path = os.path.join(BASE_DIR, 'model_features.pkl')

with open(model_path, 'wb') as f:
    pickle.dump(rf_model, f)

with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

# Save the text label encoders so your dashboard can map inputs properly
with open(features_path, 'wb') as f:
    pickle.dump({'encoders': label_encoders, 'target_mapping': target_encoder}, f)

print("\nAll artifacts exported successfully:")
print(f" -> {model_path}")
print(f" -> {scaler_path}")
print(f" -> {features_path}")