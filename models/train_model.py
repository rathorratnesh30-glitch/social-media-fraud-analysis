import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


# ==========================================
# TRAIN MODEL FUNCTION
# ==========================================
def train_models(X, y):
    # 1. Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 2. Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 3. Initialize models
    rf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)

    xgb = XGBClassifier(
        n_estimators=50, max_depth=4, eval_metric="logloss", random_state=42
    )

    # 4. Train the models
    print("Training Random Forest and XGBoost models...")
    rf.fit(X_train_scaled, y_train)
    xgb.fit(X_train_scaled, y_train)

    # ==========================================
    # SAVE TO .PKL FILES
    # ==========================================
    # Ensure the directory exists
    output_dir = "models"
    os.makedirs(output_dir, exist_ok=True)

    # Save Random Forest Model
    rf_path = os.path.join(output_dir, "fraud_rf_model.pkl")
    with open(rf_path, "wb") as file:
        pickle.dump(rf, file)

    # Save XGBoost Model
    xgb_path = os.path.join(output_dir, "fraud_xgb_model.pkl")
    with open(xgb_path, "wb") as file:
        pickle.dump(xgb, file)

    # CRITICAL: Save the scaler! (Your Streamlit app needs this to scale inputs)
    scaler_path = os.path.join(output_dir, "scaler.pkl")
    with open(scaler_path, "wb") as file:
        pickle.dump(scaler, file)

    print(f"Success! Models and scaler saved in the '{output_dir}' directory.")

    return rf, xgb, scaler, X_test_scaled, y_test
# At the very bottom of models/train_model.py:
if __name__ == "__main__":
    import numpy as np

    print("Generating random social media dataset...")
    # Generate mock data: 100 samples, 10 features each
    X_random = np.random.rand(100, 10)
    # Generate mock binary labels (0 = Real account, 1 = Fraud)
    y_random = np.random.randint(0, 2, size=100)

    # Call your fixed function
    train_models(X_random, y_random)