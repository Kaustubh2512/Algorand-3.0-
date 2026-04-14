# scanner.py
import os
import json
from utils.feature_extractor import extract_features_from_teal
from utils.feature_engineer import engineer_features
from ml_models.inference import predict
from dotenv import load_dotenv

load_dotenv()

def scan_contract(contract_code: str) -> dict:
    """
    Analyze a TEAL smart contract for security vulnerabilities using the locally trained ML model.

    Args:
        contract_code: Raw string of the smart contract code

    Returns:
        dict with score, risk_level, vulnerabilities, summary
    """
    print("=== SCANNER DEBUG (ML MODEL) ===")
    print(f"Contract length: {len(contract_code)} characters")

    if not contract_code or not contract_code.strip():
        return {
            "score": 0,
            "risk_level": "Critical",
            "vulnerabilities": [],
            "summary": "Empty contract provided."
        }

    try:
        # Extract base features
        extracted = extract_features_from_teal(contract_code)
        
        # Add engineered features
        engineered = engineer_features(extracted.copy())
        
        # Predict using the custom ML model
        prediction_num, prediction_label = predict(engineered)
        
        print(f"ML Prediction: Num={prediction_num}, Label={prediction_label}")

        label_lower = prediction_label.lower()
        
        # Map label to our standard risk levels
        if "safe" in label_lower or "low" in label_lower:
            base_score = 100
        elif "vulnerable" in label_lower or "critical" in label_lower or "high" in label_lower:
            base_score = 40
        else: # suspicious, risky, medium
            base_score = 70

        # Construct vulnerabilities based on missing checks
        vulnerabilities = []
        
        if extracted.get("has_rekey_check") == 0:
            vulnerabilities.append({
                "line": 0,
                "vulnerability_type": "UNCHECKED_REKEY",
                "issue": "RekeyTo field not verified to be zero address.",
                "severity": "Critical",
                "suggestion": "Add assert(Txn.rekey_to() == Global.zero_address())"
            })
            base_score -= 15

        if extracted.get("has_close_check") == 0:
            vulnerabilities.append({
                "line": 0,
                "vulnerability_type": "UNCHECKED_CLOSE_REMAINDER",
                "issue": "CloseRemainderTo field not explicitly rejected.",
                "severity": "High",
                "suggestion": "Add assert(Txn.close_remainder_to() == Global.zero_address())"
            })
            base_score -= 10

        if extracted.get("has_receiver_check") == 0:
            vulnerabilities.append({
                "line": 0,
                "vulnerability_type": "UNCHECKED_ASSET_RECEIVER",
                "issue": "AssetReceiver or Receiver might not be validated.",
                "severity": "Medium",
                "suggestion": "Ensure the receiver is validated in all transfer transactions."
            })
            base_score -= 5

        # Enforce score bounds
        final_score = max(0, min(100, base_score))

        # Re-enforce risk level based on the newly calculated score
        if final_score <= 40:
            risk_level = "Critical"
        elif final_score <= 70:
            risk_level = "Risky"
        else:
            risk_level = "Safe"

        summary = f"Custom ML model evaluated this contract as {prediction_label}. "
        if len(vulnerabilities) > 0:
            summary += f"Identified {len(vulnerabilities)} structural concerns missing standard checks."
        else:
            summary += "Standard security checks appear to be present."

        return {
            "score": final_score,
            "risk_level": risk_level,
            "vulnerabilities": vulnerabilities,
            "summary": summary
        }

    except Exception as e:
        print(f"[AlgoShield ML Scanner] Unexpected error: {e}")
        return {
            "score": 50,
            "risk_level": "Risky",
            "vulnerabilities": [],
            "summary": "ML Scan failed due to an unexpected error.",
            "error": str(e)
        }
