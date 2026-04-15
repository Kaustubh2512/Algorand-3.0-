# 🛡️ AlgoShield AI — Smart Contract Security Redefined

![AlgoShield Banner](https://img.shields.io/badge/Algorand-3.0_Hackathon-blue?style=for-the-badge&logo=algorand)
![AI-Powered](https://img.shields.io/badge/AI--Powered-Security-00ff88?style=for-the-badge)
![Built for Developers](https://img.shields.io/badge/Built_for-Developers-white?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=for-the-badge)

**AlgoShield AI** is an advanced security ecosystem for the Algorand blockchain. By fusing Machine Learning (ML) classification with a deterministic Rules Engine, AlgoShield provides developers with instantaneous, deep-source auditing and cryptographic proof of security through ARC-69 NFT certificates.

---

## 🌌 The Vision
In the rapidly evolving world of Algorand DeFi and NFT ecosystems, smart contract code is the law—but code often hides vulnerabilities. Manual audits are slow and expensive. **AlgoShield AI** democratizes security by providing:
- **Instant Audits**: Upload TEAL logic and get a score in seconds.
- **Hybrid Intelligence**: Combining the pattern-recognition of ML with the precision of static analysis.
- **On-Chain Reputation**: Automatic minting of Security Certificates for high-quality code.

---

## 🏗️ Project Architecture

The ecosystem consists of four interconnected components:

### 1. 📟 AI Security Engine (`/projects/backend`)
The high-performance core built with **FastAPI**.
- **Inference**: Uses a **Random Forest Classification** model trained on thousands of TEAL vulnerability patterns.
- **Static Analysis**: A custom Python-based rules engine that identifies reentrancy, overflow, and logic flaws line-by-line.
- **Persistence**: **MongoDB Atlas** for scalable scan history and certificate tracking.

### 2. 💎 Security Dashboard (`/projects/frontend`)
A premium, dark-mode terminal interface for end-users.
- **Tech**: React 18, Vite, Tailwind CSS, Framer Motion.
- **Experience**: "Terminal Luxury" aesthetic with real-time HUD animations and Pera Connect integration.

### 3. 🛡️ Developer SDK (`/projects/algoshield-sdk`)
A CLI-first approach to security.
- **Usage**: `algoshield scan <path>`
- **Workflow**: Integrate directly into CI/CD or local development loops.

### 4. ⛓️ Blockchain Layer
- **Standard**: ARC-69 NFT Certificates on Algorand Testnet.
- **Threshold**: Only contracts scoring **70/100** or higher are eligible for on-chain certification.

---

## 🚀 Installation & Local Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 20+**
- **MongoDB Atlas** account (or local MongoDB)
- **Pera Wallet** (for the frontend interaction)

---

### Phase 1: Backend Setup
1. **Navigate to backend**:
   ```bash
   cd projects/backend
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Config**:
   Copy `.env.template` to `.env` and fill in your credentials:
   ```bash
   cp .env.template .env
   ```
   *Note: Ensure `MONGODB_URL` and `PLATFORM_MNEMONIC` are set for full functionality.*
4. **Launch**:
   ```bash
   uvicorn app:app --reload
   ```

---

### Phase 2: Frontend Setup
1. **Navigate to frontend**:
   ```bash
   cd projects/frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Run Dev Server**:
   ```bash
   npm run dev
   ```
   *The dashboard will be available at `http://localhost:5173`*

---

### Phase 3: SDK Integration
1. **Navigate to SDK**:
   ```bash
   cd projects/algoshield-sdk
   ```
2. **Setup**:
   ```bash
   npm install -g .
   ```
3. **Scan a file**:
   ```bash
   algoshield scan ./my_contract.teal
   ```

---

## 📑 API Endpoints (Documentation)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/analyze` | Upload `.teal` file for hybrid audit. |
| `GET` | `/scans/{wallet}` | Retrieve history for a specific wallet address. |
| `POST` | `/mint-certificate` | Mint ARC-69 NFT for a high-scoring scan. |
| `GET` | `/health` | System health and version status. |

---

## 🤝 The Team
Developed with ❤️ by **TEAM QANTAS** for the **Algorand 3.0 Hackathon**.
- **Objective**: To make Algorand the safest blockchain for the next billion users.

---

*Securing the decentralized future, one block at a time.*
