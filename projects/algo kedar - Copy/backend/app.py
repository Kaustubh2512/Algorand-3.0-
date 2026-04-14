from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.feature_extractor import extract_features_from_teal
from utils.feature_engineer import engineer_features
from models.inference import predict

app = FastAPI(title="AlgoShieldAI Backend", description="Machine learning based security analysis for TEAL smart contracts")

# Add CORS Support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_smart_contract(file: UploadFile = File(...)):
    if not file.filename.endswith('.teal'):
        raise HTTPException(status_code=400, detail="Only .teal files are allowed")
        
    try:
        content_bytes = await file.read()
        content = content_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")
        
    try:
        # Extract base features
        extracted = extract_features_from_teal(content)
        
        # Add engineered features
        engineered = engineer_features(extracted)
        
        # Predict using the ML model
        prediction_num, prediction_label = predict(engineered)
        
        return {
            "prediction": prediction_num,
            "label": prediction_label,
            "features": engineered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
