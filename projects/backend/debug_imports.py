import sys
import os

AI_BACKEND_DIR = os.path.abspath(r"c:\Projects\Algorand 3.0\algo kedar\AlgoShield_AI\backend")
sys.path.append(AI_BACKEND_DIR)

print(f"Checking path: {AI_BACKEND_DIR}")
print(f"Exists: {os.path.exists(AI_BACKEND_DIR)}")

try:
    from utils.feature_extractor import extract_features_from_teal
    print("Successfully imported extract_features_from_teal")
except Exception as e:
    print(f"Failed to import extract_features_from_teal: {e}")

try:
    from utils.feature_engineer import engineer_features
    print("Successfully imported engineer_features")
except Exception as e:
    print(f"Failed to import engineer_features: {e}")

try:
    from models.inference import predict
    print("Successfully imported predict")
except Exception as e:
    print(f"Failed to import predict: {e}")
