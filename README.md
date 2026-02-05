# Blockchain Transaction Explainer

AI-powered blockchain transaction analysis that transforms complex transactions into clear, actionable insights.

![Blockchain Transaction Explainer](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![React](https://img.shields.io/badge/react-18.2-61dafb)
![License](https://img.shields.io/badge/license-MIT-green)

## 🚀 Features

- **Transaction Decoding**: Fetch and decode any Ethereum transaction
- **Fraud Detection**: ML-powered risk assessment
- **Gas Analysis**: Predicted vs actual gas comparison
- **Transaction Classification**: Categorize transactions (Transfer, Swap, NFT, etc.)
- **Natural Language Explanations**: AI-generated human-readable insights
- **Visual Analytics**: Interactive charts and visualizations

## 🏗️ Architecture

```
Frontend (React + Vite)
    ↓
Backend API (FastAPI)
    ↓
ML Models (Scikit-learn)
    ↓
Blockchain RPC (Ethereum)
```

## 📁 Project Structure

```
blockchain/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── routes/
│   │   ├── transaction.py      # Transaction decoding endpoints
│   │   ├── prediction.py       # ML prediction endpoints
│   │   └── explanation.py      # Explanation generation
│   ├── services/
│   │   ├── blockchain_service.py   # Web3 RPC interactions
│   │   ├── model_loader.py         # ML model loading
│   │   └── feature_extractor.py    # Feature engineering
│   ├── explainer/
│   │   └── explanation_engine.py   # NLG explanation generation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── TransactionInput.jsx
│   │   │   ├── ExplanationPanel.jsx
│   │   │   └── charts/
│   │   │       ├── FraudRiskMeter.jsx
│   │   │       ├── GasComparisonChart.jsx
│   │   │       └── TokenFlowDiagram.jsx
│   │   └── services/
│   │       └── api.js
│   ├── package.json
│   └── tailwind.config.js
├── fraud_model.pkl             # Pretrained fraud detection model
├── fraud_features.pkl          # Feature specifications
├── gas_fee_model.pkl           # Gas prediction model
├── gas_features.pkl
├── tx_classifier.pkl           # Transaction classifier
└── tx_features.pkl
```

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your RPC API keys
# Get free API key from https://www.alchemy.com or https://infura.io
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file (optional)
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

## 🚀 Running the Application

### Start Backend

```bash
cd backend

# Development mode
python main.py
# or
uvicorn main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### Start Frontend

```bash
cd frontend

# Development mode
npm run dev
```

Frontend will be available at: http://localhost:3000

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/decode_tx` | POST | Decode a transaction hash |
| `/api/predict/fraud` | POST | Get fraud risk prediction |
| `/api/predict/gas` | POST | Get gas fee prediction |
| `/api/predict/tx_type` | POST | Classify transaction type |
| `/api/explain` | POST | Get full transaction explanation |
| `/health` | GET | Health check |

### Example Request

```bash
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"tx_hash": "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"}'
```

## 🤖 ML Models

The system uses three pretrained models:

1. **Fraud Detection Model** (`fraud_model.pkl`)
   - Binary classification for fraud risk
   - Features: transaction patterns, wallet behavior

2. **Gas Fee Model** (`gas_fee_model.pkl`)
   - Regression for gas price prediction
   - Features: network congestion, transaction complexity

3. **Transaction Classifier** (`tx_classifier.pkl`)
   - Multi-class classification
   - Categories: Transfer, Swap, NFT, Staking, etc.

## 🌐 Deployment

### Backend (Render / AWS)

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel / Netlify)

```bash
# Build command
npm run build

# Output directory
dist
```

### Environment Variables

**Backend:**
- `RPC_URL` - Ethereum RPC endpoint
- `ALCHEMY_API_KEY` - Alchemy API key (optional)
- `INFURA_API_KEY` - Infura API key (optional)
- `MODELS_DIR` - Path to model files

**Frontend:**
- `VITE_API_URL` - Backend API URL

## 📊 Sample Output

```json
{
  "tx_hash": "0x...",
  "summary": "Success Simple Transfer: 1.5000 ETH transferred",
  "natural_explanation": "You transferred 1.5 ETH from 0xabc...123 to 0xdef...456. This is classified as a Simple Transfer (confidence: 92%). Gas fees were within normal range at 25.5 gwei. Fraud risk is low based on wallet behavior analysis.",
  "fraud_analysis": {
    "risk_score": 0.12,
    "risk_level": "LOW",
    "risk_factors": ["No significant risk factors identified"]
  },
  "gas_analysis": {
    "predicted_gas_gwei": 23.5,
    "actual_gas_gwei": 25.5,
    "efficiency": "NORMAL"
  },
  "classification": {
    "category": "Simple Transfer",
    "confidence": 0.92
  }
}
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT License - feel free to use this project for any purpose.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues and feature requests, please open a GitHub issue.
