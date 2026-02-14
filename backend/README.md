# Backend Service

This directory contains the FastAPI backend for the Blockchain Transaction Explainer.

## Configuration

Ensure that the ML models are loaded correctly by updating the paths in your config or main application file.

**Path Update Required:**
Previously, models might have been loaded from `backend/models/` or root. Now, they are located in `../models/`.

Update your model loading logic (e.g., in `main.py` or a specialized loader service) to reference:
- `../models/fraud_model.pkl`
- `../models/gas_fee_model.pkl`
- `../models/tx_classifier.pkl`

And respective feature files.

## Running the Server

```bash
uvicorn main:app --reload
```
