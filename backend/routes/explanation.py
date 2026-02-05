"""
Explanation engine routes - Enhanced with accurate classification and calibrated explanations
Implements all 6 fixes for improved technical accuracy
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import re

from services.blockchain_service import BlockchainService
from services.feature_extractor import FeatureExtractor
from services.model_loader import ModelLoader
from explainer.explanation_engine import ExplanationEngine


router = APIRouter()


class ExplainRequest(BaseModel):
    """Request model for full transaction explanation"""
    tx_hash: str = Field(..., pattern="^0x[a-fA-F0-9]{64}$")
    include_visualizations: bool = True
    language: str = Field(default="en", description="Explanation language (en, es, fr)")


class ExplanationSection(BaseModel):
    """A section of the explanation"""
    title: str
    content: str
    importance: str  # high, medium, low
    icon: str


class VisualizationData(BaseModel):
    """Data for frontend visualizations"""
    gas_chart: Dict[str, Any]
    fraud_gauge: Dict[str, Any]
    value_scale: Dict[str, Any]
    flow_diagram: Dict[str, Any]


class FullExplanation(BaseModel):
    """Complete explanation response"""
    tx_hash: str
    summary: str
    sections: List[ExplanationSection]
    
    # Transaction details
    transaction: Dict[str, Any]
    
    # Predictions
    fraud_analysis: Dict[str, Any]
    gas_analysis: Dict[str, Any]
    classification: Dict[str, Any]
    
    # Visualization data
    visualizations: Optional[VisualizationData]
    
    # Natural language explanation
    natural_explanation: str
    
    # Context insight (FIX #5)
    context_insight: Optional[str]
    
    # Recommendations
    recommendations: List[str]
    
    # Metadata
    generated_at: str
    confidence_score: float


@router.post("/explain", response_model=FullExplanation)
async def explain_transaction(request: ExplainRequest):
    """
    Generate a complete human-readable explanation of a blockchain transaction.
    
    Enhanced with:
    - Accurate transaction classification (Fix #1)
    - Token name detection (Fix #2)
    - Calibrated gas explanations (Fix #3)
    - Fraud risk statements (Fix #4)
    - Contextual insights (Fix #5)
    - Standardized output format (Fix #6)
    """
    try:
        # Validate hash
        if not re.match(r'^0x[a-fA-F0-9]{64}$', request.tx_hash):
            raise HTTPException(status_code=400, detail="Invalid transaction hash format")
        
        # Initialize services
        blockchain_service = BlockchainService()
        feature_extractor = FeatureExtractor()
        explanation_engine = ExplanationEngine()
        
        # 1. Fetch and decode transaction (includes token detection - Fix #2)
        tx_data = await blockchain_service.get_transaction(request.tx_hash)
        if not tx_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        receipt = await blockchain_service.get_transaction_receipt(request.tx_hash)
        decoded_tx = await blockchain_service.decode_transaction(tx_data, receipt)
        
        # 2. Extract features for ML models
        features = feature_extractor.extract_all_features(tx_data, receipt)
        
        # 3. Run fraud analysis
        fraud_result = await run_fraud_analysis(features, feature_extractor)
        
        # 4. Run gas analysis with ML prediction, then calibrate (Fix #3)
        gas_prediction = await get_gas_prediction(features)
        gas_result = explanation_engine.analyze_gas(decoded_tx, gas_prediction)
        gas_result["available"] = True
        gas_result["confidence"] = 0.85
        
        # 5. Run classification with enhanced logic (Fix #1)
        classification_result = explanation_engine.classify_transaction(decoded_tx)
        
        # Also get ML classification for comparison
        ml_classification = await run_ml_classification(features, decoded_tx)
        classification_result["ml_category"] = ml_classification.get("category")
        classification_result["all_categories"] = ml_classification.get("all_categories", {})
        
        # 6. Generate natural language explanation (Fix #6 format)
        explanation = explanation_engine.generate_explanation(
            decoded_tx=decoded_tx,
            fraud_analysis=fraud_result,
            gas_analysis=gas_result,
            classification=classification_result,
            language=request.language
        )
        
        # 7. Generate context insight (Fix #5)
        context_insight = explanation_engine.generate_context_insight(decoded_tx, classification_result)
        
        # 8. Generate visualization data
        visualizations = None
        if request.include_visualizations:
            visualizations = explanation_engine.generate_visualization_data(
                decoded_tx=decoded_tx,
                fraud_analysis=fraud_result,
                gas_analysis=gas_result,
                classification=classification_result
            )
        
        # 9. Generate recommendations
        recommendations = explanation_engine.generate_recommendations(
            fraud_analysis=fraud_result,
            gas_analysis=gas_result,
            classification=classification_result
        )
        
        # 10. Build sections for UI
        sections = explanation_engine.build_sections(
            decoded_tx=decoded_tx,
            fraud_analysis=fraud_result,
            gas_analysis=gas_result,
            classification=classification_result
        )
        
        # Calculate overall confidence
        confidence_score = (
            fraud_result.get("confidence", 0.8) * 0.3 +
            gas_result.get("confidence", 0.8) * 0.3 +
            classification_result.get("confidence", 0.8) * 0.4
        )
        
        from datetime import datetime
        
        return FullExplanation(
            tx_hash=request.tx_hash,
            summary=explanation["summary"],
            sections=sections,
            transaction=decoded_tx,
            fraud_analysis=fraud_result,
            gas_analysis=gas_result,
            classification=classification_result,
            visualizations=visualizations,
            natural_explanation=explanation["full_text"],
            context_insight=context_insight,
            recommendations=recommendations,
            generated_at=datetime.utcnow().isoformat(),
            confidence_score=round(confidence_score, 3)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")


async def run_fraud_analysis(features: Dict, feature_extractor: FeatureExtractor) -> Dict:
    """Run fraud prediction model"""
    try:
        model = ModelLoader.get_fraud_model()
        features_info = ModelLoader.get_fraud_features()
        
        if model is None:
            return {
                "risk_score": 0.15,  # Default low risk
                "risk_level": "LOW",
                "confidence": 0.5,
                "risk_factors": ["Unable to analyze - using default assessment"],
                "available": False
            }
        
        import numpy as np
        
        fraud_features = feature_extractor.prepare_fraud_features(
            features.get("wallet_features", {}), 
            features_info
        )
        
        features_array = np.array([fraud_features])
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_array)[0]
            risk_score = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
        else:
            risk_score = float(model.predict(features_array)[0])
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = "LOW"
        elif risk_score < 0.6:
            risk_level = "MEDIUM"
        elif risk_score < 0.8:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        return {
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "confidence": round(1 - abs(0.5 - risk_score) * 0.5, 2),
            "risk_factors": feature_extractor.identify_risk_factors(features.get("wallet_features", {})),
            "available": True
        }
    except Exception as e:
        return {
            "risk_score": 0.15,
            "risk_level": "LOW",
            "confidence": 0.5,
            "risk_factors": [f"Analysis error: {str(e)}"],
            "available": False
        }


async def get_gas_prediction(features: Dict) -> float:
    """Get gas prediction from ML model"""
    try:
        model = ModelLoader.get_gas_model()
        features_info = ModelLoader.get_gas_features()
        
        if model is None:
            return 25.0  # Default reasonable gas price
        
        import numpy as np
        from services.feature_extractor import FeatureExtractor
        
        feature_extractor = FeatureExtractor()
        gas_features = feature_extractor.prepare_gas_features(
            features.get("gas_features", {}),
            features_info
        )
        
        features_array = np.array([gas_features])
        predicted_gas = float(model.predict(features_array)[0])
        return max(predicted_gas, 1.0)
    except:
        return 25.0  # Default fallback


async def run_ml_classification(features: Dict, decoded_tx: Dict) -> Dict:
    """Run ML transaction classification model"""
    try:
        model = ModelLoader.get_tx_classifier()
        features_info = ModelLoader.get_tx_features()
        
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
        
        if model is None:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "all_categories": {},
                "available": False
            }
        
        import numpy as np
        from services.feature_extractor import FeatureExtractor
        
        feature_extractor = FeatureExtractor()
        tx_features = feature_extractor.prepare_tx_features(
            features.get("tx_features", {}),
            features_info
        )
        
        features_array = np.array([tx_features])
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features_array)[0]
            prediction_idx = int(np.argmax(probabilities))
            confidence = float(probabilities[prediction_idx])
            all_categories = {
                categories[i] if i < len(categories) else f"Category_{i}": 
                round(float(p), 4) 
                for i, p in enumerate(probabilities)
            }
        else:
            prediction_idx = int(model.predict(features_array)[0])
            confidence = 0.8
            all_categories = {}
        
        category = categories[prediction_idx] if prediction_idx < len(categories) else "Other"
        
        return {
            "category": category,
            "confidence": round(confidence, 4),
            "all_categories": all_categories,
            "available": True
        }
    except Exception as e:
        return {
            "category": "Unknown",
            "confidence": 0.0,
            "all_categories": {},
            "error": str(e),
            "available": False
        }


@router.get("/explain/{tx_hash}/summary")
async def get_quick_summary(tx_hash: str):
    """
    Get a quick one-line summary of a transaction
    """
    try:
        blockchain_service = BlockchainService()
        tx_data = await blockchain_service.get_transaction(tx_hash)
        
        if not tx_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        receipt = await blockchain_service.get_transaction_receipt(tx_hash)
        decoded_tx = await blockchain_service.decode_transaction(tx_data, receipt)
        
        explanation_engine = ExplanationEngine()
        summary = explanation_engine.generate_quick_summary(decoded_tx)
        
        # Also get classification
        classification = explanation_engine.classify_transaction(decoded_tx)
        
        return {
            "tx_hash": tx_hash,
            "summary": summary,
            "classification": classification.get("category"),
            "value_tier": classification.get("value_tier")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
