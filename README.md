# 🛡️ AlgoShield AI — Smart Contract Security redefined on Algorand

![AlgoShield Banner](https://img.shields.io/badge/Algorand-3.0_Hackathon-blue?style=for-the-badge&logo=algorand)
![AI-Powered](https://img.shields.io/badge/AI--Powered-Security-00ff88?style=for-the-badge)
![Built for Developers](https://img.shields.io/badge/Built_for-Developers-white?style=for-the-badge)

**AlgoShield AI** is an all-in-one security ecosystem for Algorand developers. It combines advanced Machine Learning with on-chain reputation to ensure every smart contract on Algorand is safe, audited, and certified.

---

## 🌌 The Vision
Smart contract vulnerabilities cost the ecosystem millions. **AlgoShield AI** automates the audit process, providing instant, AI-driven security scores and formal on-chain certificates, turning security from a bottleneck into a competitive advantage.

---

## 🏗️ The Ecosystem

The project is divided into four core pillars:

### 1. 📟 AI Security Engine (Backend)
The "Brain" of AlgoShield. Built with **FastAPI** and **Python**, it uses a **Random Forest Classification model** to analyze TEAL logic.
- **Location**: `/projects/backend`
- **Logic**: Hybrid Intelligence model (ML + Rules Engine).
- **Features**: Real-time analysis, vulnerability mapping, and scan history.

### 2. 💎 Security Dashboard (Frontend)
A premium, dark-themed command center for developers to manage their contract security.
- **Location**: `/projects/frontend`
- **Tech**: React, Tailwind CSS, Framer Motion.
- **Features**: Live terminal-style scanning, recent scan history, and NFT management.

### 3. 🛡️ Developer SDK
A dedicated SDK that brings AlgoShield security directly to the developer's CLI or CI/CD pipeline.
- **Location**: `/projects/algoshield-sdk`
- **Features**: Global CLI tool (`algoshield`), real-time file watcher, and programmatic auditing.

### 4. ⛓️ Blockchain Layer (Certificates)
Official on-chain verification using **Algorand Testnet**.
- **Standard**: ARC-69 NFT Security Certificates.
- **Process**: Scores ≥ 70 trigger a minting event, delivering a permanent cryptographic proof of security to the developer's Pera Wallet.

---

## 🛠️ Tech Stack

- **Blockchain**: Algorand (py-algorand-sdk, ARC-69)
- **AI/ML**: Python, Scikit-learn, Joblib (Random Forest Model)
- **Backend**: FastAPI, MongoDB (Scan persistence)
- **Frontend**: React (Vite), Tailwind CSS, Pera Connect
- **SDK**: Node.js, Chokidar, Axios

---

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd projects/backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### 2. Start the Frontend
```bash
cd projects/frontend
npm install
npm run dev
```

### 3. Use the SDK (Local Audit)
```bash
cd projects/algoshield-sdk
npm install
node bin/algoshield.js scan ./my-contract.teal
```

---



## 🤝 Team
Developed with ❤️ by **TEAM QANTAS** for the **Algorand 3.0 Hackathon**.

*Securing the decentralized future, one block at a time.*
