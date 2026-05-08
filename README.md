# 🛡️ AlgoShield AI — Next-Gen Smart Contract Security on Algorand

![AlgoShield Banner](https://img.shields.io/badge/Algorand-3.0_Hackathon-blue?style=for-the-badge&logo=algorand)
![AI-Powered](https://img.shields.io/badge/AI--Powered-Security-00ff88?style=for-the-badge)
![Built for Developers](https://img.shields.io/badge/Built_for-Developers-white?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)

**AlgoShield AI** is an all-in-one security ecosystem for Algorand developers. It combines advanced Machine Learning, Small Language Models (SLMs), and 24/7 live on-chain monitoring to ensure every smart contract on Algorand is safe, audited, and certified.

---

## 🌌 The Vision
Smart contract vulnerabilities cost the ecosystem millions. **AlgoShield AI** automates the entire audit lifecycle. From the moment you write your code to the moment it's deployed on mainnet, AlgoShield provides instant AI-driven security scores, actionable RAG-based code fixes, on-chain certificates, and continuous live monitoring. 

Turn security from a bottleneck into your competitive advantage.

---

## ✨ Key Features & Use Cases

### 1. 📟 AI Security Scanner & Suggestion Engine (RAG)
Upload your `.teal` file or provide an Algorand App ID to get an instant vulnerability report. 
- **Hybrid Intelligence:** Uses a Random Forest ML model alongside a strict rule-based engine to classify contract risk.
- **AI Fix Suggestions:** Powered by a local Phi-3-mini SLM and ChromaDB Vectorstore. It provides highly accurate, line-by-line fix recommendations based on a curated Algorand security knowledge base.

### 2. 📡 24/7 Live On-Chain Monitoring
Never take your eyes off your deployed contracts.
- **Anomaly Detection:** Continuously polls the Algorand Indexer for new transactions and feeds them into an Isolation Forest ML model to detect anomalous activities (e.g., Reentrancy, balance drains).
- **Email Alerts:** Automatically dispatches rich HTML email alerts to developers the moment a critical risk is flagged on-chain.

### 3. 💎 Interactive Security Dashboard
A premium, dark-themed command center for developers.
- **Live Terminal-Style Scanning:** Visual, modern UI to read security reports.
- **NFT Certificate Minting:** If a contract scores ≥ 70, you can officially mint an ARC-69 NFT Security Certificate directly to your Pera Wallet on the Algorand blockchain.
- **Monitoring Hub:** View live transaction feeds and configure alert settings.

### 4. 🛡️ Developer SDK & CLI
Bring AlgoShield directly into your terminal or CI/CD pipeline.
- Automatically scan files locally and watch for changes while you develop.

---

## 🚀 Installation & Local Setup

### Tech Stack
- **Blockchain**: Algorand SDK (`py-algorand-sdk`), ARC-69 NFT Standard, Algonode Indexer
- **AI/ML**: Python, Scikit-learn (Random Forest, Isolation Forest), `llama-cpp-python` (Phi-3-mini), ChromaDB
- **Backend**: FastAPI, Motor (Async MongoDB), APScheduler, Python `smtplib`
- **Frontend**: React (Vite), Tailwind CSS, Framer Motion, Pera Connect
- **SDK**: Node.js, Chokidar, Axios

---

## 🚀 Getting Started

Follow these steps to run the complete AlgoShield AI platform on your local machine.

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**
- **MongoDB** (running locally on port `27017` or via MongoDB Atlas)
- **C/C++ Build Tools** (Required for installing `llama-cpp-python` and `chromadb` on some OS)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AlgoShield_AI.git
cd AlgoShield_AI/projects
```

### 2. Configure Environment Variables
Navigate to the `projects/backend` directory and create a `.env` file:
```bash
cd backend
touch .env
```
Populate the `.env` file with the following variables:
```env
# MongoDB Connection
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=algoshield

# SMTP Email Alerting (Use Gmail App Password)
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
ALERT_FROM_EMAIL=AlgoShield AI <your-email@gmail.com>

# Algorand Indexer (Optional - defaults to algonode)
INDEXER_API_URL=https://mainnet-idx.algonode.cloud
```

### 3. Start the Backend API
Install the Python dependencies and run the server. (It is highly recommended to use a virtual environment).
```bash
# Inside projects/backend
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate
# Activate venv (Mac/Linux)
source venv/bin/activate

pip install -r requirements.txt

# Run the backend
python app.py
```
*Note: The first time you request AI suggestions, the backend will automatically download the Phi-3-mini model from HuggingFace.*

### 4. Start the Frontend Dashboard
Open a new terminal window, navigate to the frontend directory, and start the Vite development server.
```bash
cd projects/frontend
npm install
npm run dev
```
Visit `http://localhost:5173` in your browser.

### 5. Run the CLI SDK (Optional)
To test contracts directly from your terminal:
```bash
cd projects/algoshield-sdk
npm install
node bin/algoshield.js scan ./my-contract.teal
```

---

## 🤝 Team
Developed with ❤️ by **TEAM QANTAS** for the **Algorand 3.0 Hack Series 🐍**.

*Securing the decentralized future, one block at a time.*
