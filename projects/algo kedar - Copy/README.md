# AlgoShieldAI

AlgoShieldAI is an intelligent, machine-learning-powered security analysis system for Algorand smart contracts written in TEAL. It classifies smart contracts into three risk categories based on structural features and known vulnerabilities.

## Features
- **Machine Learning Core**: A trained Random Forest model that evaluates the security logic, transaction density, and specific guard checks (e.g. `RekeyTo`, `CloseRemainderTo`).
- **Headless Backend**: Modern, lightweight FastAPI service for robust and concurrent REST API endpoints.
- **Dynamic Frontend**: A visually stunning 3D glassmorphism React interface featuring drag-and-drop .teal file uploads and instant security assessment highlighting.
- **End-to-End Predictable Processing**: Extracts raw code, applies feature engineering in real-time without recompiling the model, maintaining high availability.

## Tech Stack
- **Machine Learning**: Scikit-Learn, Joblib, Numpy
- **Backend API**: Python, FastAPI, Uvicorn
- **Frontend UI**: React, JavaScript, Vite, Vanilla CSS 

## Project Structure
```text
AlgoShieldAI/
├── contracts/               # Original TEAL test contracts (Safe, Vulnerable, Risky)
├── dataset/                 # Raw/engineered data structures (.csv logs)
├── model/                   # Serialized ML artifacts (.pkl)
├── backend/                 # FastAPI REST API implementation
│   ├── app.py
│   ├── models/              # Inference scripts interacting with Joblib
│   └── utils/               # Feature generation & extraction modules
└── frontend/                # React.js SPA Application
```

## How It Works
1. **Client Action**: The user securely uploads a `.teal` contract through the React Frontend.
2. **Analysis Pipeline**: The FastAPI backend catches the payload in-memory (no database required) and tokenizes the code layout.
3. **Feature Engineering**: Algorand-specific security heuristics are calculated dynamically—such as logical operator density (`&&`, `||`), security check omissions, and raw operational length sizing.
4. **Machine Learning Inference**: The pre-trained Random Forest model yields a risk classification and serializes it in JSON mapping it cleanly to SAFE, SUSPICIOUS, or RISKY labels.

## How to Run

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
The API should now be running locally at `http://127.0.0.1:8000`. Full endpoint documentation is available at `http://127.0.0.1:8000/docs`.

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173/` in any modern web browser to access the client interface. 

---
### Example API Request (For CLI/Backend Verification)
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@contracts/safe/basic.teal"
```

### Future Improvements
- Migration from naive string-based feature extraction to full Abstract Syntax Tree (AST) compilation models for TEAL.
- Deployment architectures using Docker Compose.
- Extending visual layout to display raw, highlighted TEAL code mapping back precisely to detected insecure segments.
