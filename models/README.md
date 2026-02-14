# 🧠 Trained ML Models

This directory contains the trained machine learning models and feature definitions used by the backend service.

## Artifacts

- **fraud_model.pkl**: Scikit-learn model for detecting fraudulent transaction patterns.
- **fraud_features.pkl**: Feature definitions/metadata for the fraud model.
- **gas_fee_model.pkl**: Regression model for predicting optimal gas fees.
- **gas_features.pkl**: Feature definitions for the gas model.
- **tx_classifier.pkl**: Classifier for categorizing transactions (Swap, Transfer, etc.).
- **tx_features.pkl**: Feature definitions for the classifier.

## Usage

These models are loaded by `backend/services/model_loader.py`. Ensure the path configuration in the backend points to this directory.
