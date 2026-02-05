"""
ML Prediction routes for fraud detection, gas estimation, and transaction classification
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import numpy as np

from services.model_loader import ModelLoader
from services.feature_extractor import FeatureExtractor


router = APIRouter()


class FraudPredictionRequest(BaseModel):
    """Request model for fraud prediction"""
    wallet_address: Optional[str] = None
    transaction_count: int = Field(..., ge=0)
    total_value_sent: float = Field(..., ge=0)
    total_value_received: float = Field(..., ge=0)
    unique_addresses_interacted: int = Field(..., ge=0)
    avg_transaction_value: float = Field(..., ge=0)
    max_transaction_value: float = Field(..., ge=0)
    min_transaction_value: float = Field(..., ge=0)
    avg_gas_price: float = Field(..., ge=0)
    contract_creation_count: int = Field(..., ge=0)
    failed_transaction_ratio: float = Field(..., ge=0, le=1)
    time_between_txs_avg: float = Field(..., ge=0)
    

class FraudPredictionResponse(BaseModel):
    """Response model for fraud prediction"""
    risk_score: float
    risk_level: str
    confidence: float
    risk_factors: List[str]
    recommendation: str


class GasPredictionRequest(BaseModel):
    """Request model for gas prediction"""
    value_eth: float = Field(..., ge=0)
    gas_limit: int = Field(..., ge=21000)
    is_contract_call: bool = False
    input_data_size: int = Field(default=0, ge=0)
    network_congestion: float = Field(default=0.5, ge=0, le=1)
    time_of_day: int = Field(default=12, ge=0, le=23)
    day_of_week: int = Field(default=0, ge=0, le=6)


class GasPredictionResponse(BaseModel):
    """Response model for gas prediction"""
    predicted_gas_price_gwei: float
    predicted_total_fee_eth: float
    confidence_interval: Dict[str, float]
    network_status: str
    savings_potential: Optional[str]


class TxClassificationRequest(BaseModel):
    """Request model for transaction classification"""
    value_eth: float
    gas_used: int
    input_data_length: int
    to_address_type: str  # 'eoa', 'contract', 'exchange', 'defi'
    from_address_type: str
    method_id: Optional[str] = None


class TxClassificationResponse(BaseModel):
    """Response model for transaction classification"""
    category: str
    subcategory: Optional[str]
    confidence: float
    all_categories: Dict[str, float]
    description: str


@router.post("/fraud", response_model=FraudPredictionResponse)
async def predict_fraud(request: FraudPredictionRequest):
    """
    Predict fraud risk for a wallet based on behavioral features.
    
    Uses a trained ML model to analyze wallet patterns and identify
    potentially fraudulent behavior.
    """
    try:
        model = ModelLoader.get_fraud_model()
        features_info = ModelLoader.get_fraud_features()
        
        if model is None:
            raise HTTPException(status_code=503, detail="Fraud model not loaded")
        
        # Prepare features for prediction
        feature_extractor = FeatureExtractor()
        features = feature_extractor.prepare_fraud_features(request.dict(), features_info)
        
        # Make prediction
        features_array = np.array([features])
        
        # Get probability if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_array)[0]
            risk_score = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
        else:
            prediction = model.predict(features_array)[0]
            risk_score = float(prediction)
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = "LOW"
            recommendation = "Transaction appears safe. Normal activity patterns detected."
        elif risk_score < 0.6:
            risk_level = "MEDIUM"
            recommendation = "Exercise caution. Some unusual patterns detected in wallet behavior."
        elif risk_score < 0.8:
            risk_level = "HIGH"
            recommendation = "High risk detected. Recommend further investigation before proceeding."
        else:
            risk_level = "CRITICAL"
            recommendation = "Critical risk level. Strong indicators of fraudulent activity."
        
        # Identify risk factors
        risk_factors = feature_extractor.identify_risk_factors(request.dict())
        
        return FraudPredictionResponse(
            risk_score=round(risk_score, 4),
            risk_level=risk_level,
            confidence=round(1 - abs(0.5 - risk_score) * 0.5, 2),
            risk_factors=risk_factors,
            recommendation=recommendation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fraud prediction error: {str(e)}")


@router.post("/gas", response_model=GasPredictionResponse)
async def predict_gas(request: GasPredictionRequest):
    """
    Predict optimal gas price for a transaction.
    
    Uses historical gas data and network conditions to estimate
    the most efficient gas price.
    """
    try:
        model = ModelLoader.get_gas_model()
        features_info = ModelLoader.get_gas_features()
        
        if model is None:
            raise HTTPException(status_code=503, detail="Gas model not loaded")
        
        # Prepare features
        feature_extractor = FeatureExtractor()
        features = feature_extractor.prepare_gas_features(request.dict(), features_info)
        
        # Make prediction
        features_array = np.array([features])
        predicted_gas_price = float(model.predict(features_array)[0])
        
        # Ensure non-negative prediction
        predicted_gas_price = max(predicted_gas_price, 1.0)
        
        # Calculate total fee
        gas_to_use = min(request.gas_limit, 21000 + request.input_data_size * 16)
        if request.is_contract_call:
            gas_to_use = request.gas_limit
        
        predicted_fee_eth = (predicted_gas_price * gas_to_use) / 1e9
        
        # Determine network status
        if request.network_congestion < 0.3:
            network_status = "Low congestion - Good time to transact"
            savings = "Wait for even lower gas during off-peak hours (UTC 2-6 AM)"
        elif request.network_congestion < 0.6:
            network_status = "Moderate congestion - Normal fees expected"
            savings = "Consider waiting 1-2 hours for potential savings"
        else:
            network_status = "High congestion - Elevated fees"
            savings = "Postpone non-urgent transactions if possible"
        
        return GasPredictionResponse(
            predicted_gas_price_gwei=round(predicted_gas_price, 2),
            predicted_total_fee_eth=round(predicted_fee_eth, 6),
            confidence_interval={
                "low": round(predicted_gas_price * 0.85, 2),
                "high": round(predicted_gas_price * 1.15, 2)
            },
            network_status=network_status,
            savings_potential=savings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gas prediction error: {str(e)}")


@router.post("/tx_type", response_model=TxClassificationResponse)
async def predict_transaction_type(request: TxClassificationRequest):
    """
    Classify a blockchain transaction into categories.
    
    Categories include: Transfer, Swap, NFT, Staking, Bridge, Contract Deploy, etc.
    """
    try:
        model = ModelLoader.get_tx_classifier()
        features_info = ModelLoader.get_tx_features()
        
        if model is None:
            raise HTTPException(status_code=503, detail="Transaction classifier not loaded")
        
        # Prepare features
        feature_extractor = FeatureExtractor()
        features = feature_extractor.prepare_tx_features(request.dict(), features_info)
        
        # Make prediction
        features_array = np.array([features])
        
        # Category mapping
        categories = [
            "Simple Transfer",
            "Token Transfer", 
            "DEX Swap",
            "NFT Transaction",
            "Staking/Yield",
            "Bridge Transfer",
            "Contract Deployment",
            "Governance Vote",
            "Lending/Borrowing",
            "Other"
        ]
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_array)[0]
            prediction_idx = int(np.argmax(probabilities))
            confidence = float(probabilities[prediction_idx])
            
            # Get all category probabilities
            all_categories = {
                categories[i] if i < len(categories) else f"Category_{i}": 
                round(float(p), 4) 
                for i, p in enumerate(probabilities)
            }
        else:
            prediction_idx = int(model.predict(features_array)[0])
            confidence = 0.8  # Default confidence without probabilities
            all_categories = {categories[prediction_idx]: 1.0}
        
        category = categories[prediction_idx] if prediction_idx < len(categories) else "Other"
        
        # Generate description
        descriptions = {
            "Simple Transfer": "A basic ETH transfer between two addresses",
            "Token Transfer": "Transfer of ERC-20 tokens between addresses",
            "DEX Swap": "Token exchange on a decentralized exchange",
            "NFT Transaction": "NFT purchase, sale, or transfer",
            "Staking/Yield": "Staking tokens or yield farming activity",
            "Bridge Transfer": "Cross-chain asset transfer via bridge",
            "Contract Deployment": "Deployment of a new smart contract",
            "Governance Vote": "Participation in DAO governance",
            "Lending/Borrowing": "DeFi lending or borrowing activity",
            "Other": "Transaction type could not be classified"
        }
        
        return TxClassificationResponse(
            category=category,
            subcategory=None,
            confidence=round(confidence, 4),
            all_categories=all_categories,
            description=descriptions.get(category, "Unknown transaction type")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")
