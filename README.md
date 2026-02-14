# 🔗 Blockchain Transaction Explainer

An AI-powered Web3 analytics platform that decodes blockchain transactions and converts them into human-readable explanations with fraud risk insights, gas analysis, and transaction intelligence.

![Blockchain Transaction Explainer](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![React](https://img.shields.io/badge/react-18.2-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Overview

Blockchain transactions are transparent but difficult to interpret for non-technical users. Raw transaction hashes expose low-level execution data such as gas fees, contract calls, and token transfers — but lack contextual meaning.

**Blockchain Transaction Explainer** bridges this gap by combining:

- ✅ Blockchain decoding
- ✅ Machine learning models
- ✅ Semantic classification
- ✅ Natural language generation
- ✅ Visual analytics

The result: clear, structured explanations of "what actually happened" in any blockchain transaction.

---

## 🎯 Key Objectives

| Objective | Description |
|-----------|-------------|
| 🧠 **Understandability** | Make Web3 transactions accessible to everyone |
| 🛡️ **Fraud Intelligence** | Provide risk scoring and behavioral analysis |
| ⛽ **Gas Insights** | Analyze efficiency and cost anomalies |
| 🏷️ **Auto-Classification** | Identify transaction types automatically |
| 📊 **Visual Analytics** | Present data through intuitive visualizations |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ Transaction │  │   Charts    │  │   Explanation Panel     │  │
│  │    Input    │  │  (Recharts) │  │                         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Routes     │  │   Services   │  │  Explanation Engine  │   │
│  │  /api/*      │  │  Blockchain  │  │   NLG Generation     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                    ML MODELS (.pkl)                        │  │
│  │   Fraud Detection  │  Gas Prediction  │  TX Classifier    │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ Web3.py
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ETHEREUM BLOCKCHAIN                            │
│                  (via Alchemy / Infura RPC)                      │
└─────────────────────────────────────────────────────────────────┘
```

---

# 🧠 Core Features

## 1️⃣ Transaction Decoding

- Fetches live transaction data via Ethereum RPC
- Decodes raw blockchain execution
- Extracts:
  - Sender & receiver addresses
  - Value transferred (ETH/tokens)
  - Gas used & gas price
  - Transaction status
  - Nonce & input data
- Supports both successful and failed transactions

---

## 2️⃣ Smart Transaction Classification

Automatically identifies transaction intent:

| Category | Description |
|----------|-------------|
| 💸 Native ETH Transfers | Direct wallet-to-wallet ETH |
| 🪙 ERC-20 Token Transfers | USDT, USDC, DAI movements |
| 🔄 DEX Swaps | Uniswap, SushiSwap trades |
| 🎨 NFT Transactions | OpenSea, Seaport interactions |
| 📄 Contract Deployments | New smart contract creation |
| 📈 Staking/Yield | DeFi staking operations |
| 💧 Liquidity Provision | LP token minting |

### Value Tier Classification

| Tier | ETH Value |
|------|-----------|
| Small | < 1 ETH |
| Medium | 1 – 10 ETH |
| High Value | > 10 ETH |

---

## 3️⃣ Token Detection & Metadata

- Automatic ERC-20 detection
- Fetches token symbol, name, decimals
- Preloaded major tokens:

| Token | Type |
|-------|------|
| USDT | Stablecoin |
| USDC | Stablecoin |
| DAI | Stablecoin |
| WETH | Wrapped ETH |
| UNI | Governance |
| LINK | Oracle |
| WBTC | Wrapped BTC |
| MATIC | L2 Token |

- Accurate token amount decoding

---

## 4️⃣ Known Address Recognition

Recognizes major ecosystem entities:

| Type | Examples |
|------|----------|
| 🏦 Exchanges | Binance, Coinbase |
| 🔀 DEX Routers | Uniswap V2/V3 |
| 🖼️ NFT Platforms | OpenSea, Seaport |
| 🏗️ DeFi Protocols | Aave, Compound |

Addresses are labeled with human-readable names.

---

# 🤖 AI / Machine Learning Features

## 5️⃣ Fraud Risk Detection

ML-powered behavioral analysis:

- **Risk Score**: 0–100%
- **Risk Tiers**:

| Level | Score Range | Action |
|-------|-------------|--------|
| 🟢 LOW | 0-30% | Safe to proceed |
| 🟡 MEDIUM | 30-60% | Exercise caution |
| 🟠 HIGH | 60-80% | Investigate |
| 🔴 CRITICAL | 80-100% | Do not proceed |

**Analyzes:**
- Transaction burst patterns
- Wallet clustering behavior
- Token spam activity
- Contract creation anomalies
- Failed transaction ratios

---

## 6️⃣ Gas Fee Prediction

Predicts optimal gas cost using regression models:

| Status | Interpretation | Threshold |
|--------|----------------|-----------|
| ✅ EXCELLENT | Below predicted | < -20% |
| ✅ NORMAL | Within range | ±20% |
| ⚠️ ABOVE AVERAGE | Higher than usual | +20-80% |
| 🔴 CONGESTED | Network busy | +80%+ |

- USD fee conversion included
- Calibrated explanations (no unrealistic percentages)

---

## 7️⃣ Transaction Type Classifier

Multi-class ML classifier categorizing:

- Transfers
- Swaps
- NFT trades
- Governance votes
- Lending interactions
- Bridge transfers
- Contract deployments

Includes confidence scoring and fallback heuristics.

### 📈 Model Performance

| Model | Metric | Value | Description |
|-------|--------|-------|-------------|
| **Fraud Detection** | Accuracy | 92% | Identifies fraudulent transactions with high precision |
| **Gas Fee Prediction** | MAE | 2.5 Gwei | Predicts gas fees with low mean absolute error |
| **Transaction Classifier** | F1-Score | 0.89 | Accurately classifies various transaction types |

---

# 💬 Explanation Engine

## 8️⃣ Natural Language Explanations

Generates human-readable insights in a **standardized 5-part format**:

```
1. 📋 Transaction Summary
   "You transferred 12 ETH from 0xabc...123 to Binance Hot Wallet."

2. 🏷️ Classification
   "This is classified as a High Value Native ETH Transfer."

3. ⛽ Gas Analysis
   "Gas fees were within normal range. (Fee: $2.50 USD)"

4. 🛡️ Fraud Risk Assessment
   "No suspicious wallet behavior detected."

5. 💡 Context Insight
   "This transaction resembles a large exchange deposit."
```

---

## 9️⃣ Contextual Intelligence

Adds interpretive insights such as:

- 🏦 Exchange deposit patterns
- 🐋 Whale transfer detection (>50 ETH)
- 💵 Stablecoin payment context
- 💧 Liquidity provisioning explanations
- 📊 Asset reallocation insights

---

## 🔟 Actionable Recommendations

Provides user guidance:

- ⚠️ Security alerts for risky transactions
- ⛽ Gas optimization tips
- ⏰ Transaction timing suggestions
- ✅ Wallet verification advice

---

# 📊 Visualization Features

## 1️⃣1️⃣ Fraud Risk Gauge
- 0–100% visual risk meter
- Color-coded severity levels
- Risk factor breakdown list

## 1️⃣2️⃣ Gas Comparison Chart
- Predicted vs actual bar chart
- Efficiency status badge
- USD fee display

## 1️⃣3️⃣ Transaction Flow Diagram
- Sender → Receiver → Contract flow
- Token/ETH values with icons
- Exchange & protocol labels
- Transfer magnitude indicators

## 1️⃣4️⃣ Classification Display
- Category badges with icons
- Confidence percentage indicators
- Alternative category predictions

---

# 🖥️ Frontend Features

## 1️⃣5️⃣ Premium Dark UI
- 🌙 Glassmorphism design
- 🎨 Gradient backgrounds
- ✨ Particle effects
- 🎬 Smooth animations

## 1️⃣6️⃣ Transaction Input System
- ✅ Hash validation (0x + 64 hex)
- 📋 Clipboard paste button
- 📝 Example transaction quick-fill
- ⏳ Loading states with skeletons

## 1️⃣7️⃣ Responsive Layout
- 📱 Mobile optimized
- 🔲 Adaptive grids
- 👆 Touch-friendly UI

---

# 📡 API Endpoints

| Endpoint | Method | Function |
|----------|--------|----------|
| `/api/explain` | POST | Full transaction explanation |
| `/api/explain/{hash}/summary` | GET | Quick summary |
| `/api/predict/fraud` | POST | Fraud risk prediction |
| `/api/predict/gas` | POST | Gas fee estimation |
| `/api/predict/tx_type` | POST | Transaction classification |
| `/api/decode_tx` | POST | Raw transaction decode |
| `/health` | GET | Service health status |

### Example Request

```bash
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"tx_hash": "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"}'
```

---

# 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, Tailwind CSS |
| **Charts** | Recharts |
| **Backend** | FastAPI, Python 3.9+ |
| **Blockchain** | Web3.py |
| **ML** | Scikit-learn, NumPy |
| **Models** | Joblib (.pkl files) |
| **API Client** | Axios |

---

# 🏗️ Project Structure

```
blockchain-transaction-explainer/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
│
├── 📁 models/                   # 🧠 Trained ML artifacts
│   ├── 🤖 fraud_model.pkl
│   ├── 🤖 fraud_features.pkl
│   ├── 🤖 gas_fee_model.pkl
│   ├── 🤖 gas_features.pkl
│   ├── 🤖 tx_classifier.pkl
│   ├── 🤖 tx_features.pkl
│
├── 📁 notebooks/                # 📓 Model training & experiments
│   └── 📄 README.md
│
├── 📁 screenshots/              # 📷 Application visuals
│   └── 📄 README.md
│
├── 📁 backend/                  # 🐍 FastAPI Application
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── 📁 routes/               # API Endpoints
│   │   ├── transaction.py
│   │   ├── prediction.py
│   │   └── explanation.py
│   │
│   ├── 📁 services/             # Logic Services
│   │   ├── blockchain_service.py
│   │   ├── model_loader.py
│   │   └── feature_extractor.py
│   │
│   └── 📁 explainer/            # NLG Engine
│       └── explanation_engine.py
│
└── 📁 frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    │
    └── 📁 src/
        ├── App.jsx              # Main application
        ├── main.jsx             # Entry point
        ├── index.css            # Global styles
        │
        ├── 📁 components/
        │   ├── Header.jsx
        │   ├── TransactionInput.jsx
        │   ├── ExplanationPanel.jsx
        │   ├── TransactionClassification.jsx
        │   ├── LoadingState.jsx
        │   ├── ParticleBackground.jsx
        │   │
        │   └── 📁 charts/
        │       ├── FraudRiskMeter.jsx
        │       ├── GasComparisonChart.jsx
        │       └── TokenFlowDiagram.jsx
        │
        └── 📁 services/
            └── api.js           # API integration
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

## 1️⃣ Clone Repository

```bash
git clone https://github.com/shankarsai000/Explainable-AI-for-Blockchain-Transactions.git
cd Explainable-AI-for-Blockchain-Transactions
```

## 2️⃣ Backend Setup

```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your RPC API keys

# Run server
python main.py
# or
uvicorn main:app --reload --port 8000
```

Backend available at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

## 3️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend available at: **http://localhost:5000**

## 4️⃣ Environment Variables

Create `.env` in the backend folder:

```env
# Ethereum RPC URL
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# API Keys (get free at alchemy.com or infura.io)
ALCHEMY_API_KEY=your_alchemy_key
INFURA_API_KEY=your_infura_key

# Model directory
MODELS_DIR=../

# CORS
CORS_ORIGINS=http://localhost:5000,http://localhost:3000
```

---

# 🧪 Example Output

**Input:** `0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060`

**Output:**
```json
{
  "tx_hash": "0x5c50...",
  "summary": "Success: 1.5000 ETH - Medium Native ETH Transfer",
  "natural_explanation": "You transferred 1.5 ETH from 0xabc...123 to 0xdef...456.\n\nThis is classified as a Medium Native ETH Transfer.\n\nGas fees were within normal range. (Fee: $3.25 USD)\n\nNo suspicious wallet behavior detected.\n\nThis is a standard ETH transfer between addresses.",
  "classification": {
    "category": "Medium Native ETH Transfer",
    "confidence": 0.92
  },
  "fraud_analysis": {
    "risk_score": 0.12,
    "risk_level": "LOW"
  },
  "gas_analysis": {
    "predicted_gas_gwei": 25.0,
    "actual_gas_gwei": 28.5,
    "efficiency": "NORMAL",
    "fee_usd": 3.25
  }
}
```

---

# 🌐 Deployment

## Backend (Render / AWS / Heroku)

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Frontend (Vercel / Netlify)

```bash
# Build command
npm run build

# Output directory
dist
```

---

# 🔮 Future Enhancements

- 🌐 Cross-chain support (BSC, Polygon, Arbitrum)
- 📊 Wallet risk dashboards
- ⚡ MEV detection
- 🔓 Token approval exploit alerts
- 💼 Portfolio analytics
- 🤖 GPT-powered explanations

---

# 🤝 Contributing

Pull requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

# 📜 License

MIT License — free to use, modify, and distribute.

---

# 👨‍💻 Author

Built as an AI + Blockchain analytics system to improve Web3 transparency and transaction literacy.

**GitHub:** [@shankarsai000](https://github.com/shankarsai000)

---

<p align="center">
  <b>🚀 Making Web3 Understandable for Everyone 🚀</b>
</p>
