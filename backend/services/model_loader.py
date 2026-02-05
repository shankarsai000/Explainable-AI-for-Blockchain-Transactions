"""
ML Model Loader Service
Handles loading and caching of pretrained models
"""

import os
import joblib
from typing import Optional, Any, Dict
from pathlib import Path


class ModelLoader:
    """Singleton class to manage ML model loading and access"""
    
    _fraud_model: Optional[Any] = None
    _fraud_features: Optional[Any] = None
    _gas_model: Optional[Any] = None
    _gas_features: Optional[Any] = None
    _tx_classifier: Optional[Any] = None
    _tx_features: Optional[Any] = None
    _models_loaded: bool = False
    
    # Default model directory (parent of backend folder)
    _models_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "")
    
    @classmethod
    def set_models_dir(cls, path: str):
        """Set the directory containing the model files"""
        cls._models_dir = path
    
    @classmethod
    def _get_model_path(cls, filename: str) -> str:
        """Get full path to a model file"""
        return os.path.join(cls._models_dir, filename)
    
    @classmethod
    def load_all_models(cls) -> Dict[str, bool]:
        """
        Load all ML models from the models directory.
        Returns a dict indicating which models were loaded successfully.
        """
        results = {}
        
        # Load fraud detection model
        try:
            fraud_model_path = cls._get_model_path("fraud_model.pkl")
            if os.path.exists(fraud_model_path):
                cls._fraud_model = joblib.load(fraud_model_path)
                results["fraud_model"] = True
                print(f"  ✓ Loaded fraud_model.pkl")
            else:
                print(f"  ✗ fraud_model.pkl not found at {fraud_model_path}")
                results["fraud_model"] = False
        except Exception as e:
            print(f"  ✗ Error loading fraud_model.pkl: {e}")
            results["fraud_model"] = False
        
        # Load fraud features
        try:
            fraud_features_path = cls._get_model_path("fraud_features.pkl")
            if os.path.exists(fraud_features_path):
                cls._fraud_features = joblib.load(fraud_features_path)
                results["fraud_features"] = True
                print(f"  ✓ Loaded fraud_features.pkl")
            else:
                print(f"  ✗ fraud_features.pkl not found")
                results["fraud_features"] = False
        except Exception as e:
            print(f"  ✗ Error loading fraud_features.pkl: {e}")
            results["fraud_features"] = False
        
        # Load gas fee model
        try:
            gas_model_path = cls._get_model_path("gas_fee_model.pkl")
            if os.path.exists(gas_model_path):
                cls._gas_model = joblib.load(gas_model_path)
                results["gas_model"] = True
                print(f"  ✓ Loaded gas_fee_model.pkl")
            else:
                print(f"  ✗ gas_fee_model.pkl not found")
                results["gas_model"] = False
        except Exception as e:
            print(f"  ✗ Error loading gas_fee_model.pkl: {e}")
            results["gas_model"] = False
        
        # Load gas features
        try:
            gas_features_path = cls._get_model_path("gas_features.pkl")
            if os.path.exists(gas_features_path):
                cls._gas_features = joblib.load(gas_features_path)
                results["gas_features"] = True
                print(f"  ✓ Loaded gas_features.pkl")
            else:
                print(f"  ✗ gas_features.pkl not found")
                results["gas_features"] = False
        except Exception as e:
            print(f"  ✗ Error loading gas_features.pkl: {e}")
            results["gas_features"] = False
        
        # Load transaction classifier
        try:
            tx_classifier_path = cls._get_model_path("tx_classifier.pkl")
            if os.path.exists(tx_classifier_path):
                cls._tx_classifier = joblib.load(tx_classifier_path)
                results["tx_classifier"] = True
                print(f"  ✓ Loaded tx_classifier.pkl")
            else:
                print(f"  ✗ tx_classifier.pkl not found")
                results["tx_classifier"] = False
        except Exception as e:
            print(f"  ✗ Error loading tx_classifier.pkl: {e}")
            results["tx_classifier"] = False
        
        # Load transaction features
        try:
            tx_features_path = cls._get_model_path("tx_features.pkl")
            if os.path.exists(tx_features_path):
                cls._tx_features = joblib.load(tx_features_path)
                results["tx_features"] = True
                print(f"  ✓ Loaded tx_features.pkl")
            else:
                print(f"  ✗ tx_features.pkl not found")
                results["tx_features"] = False
        except Exception as e:
            print(f"  ✗ Error loading tx_features.pkl: {e}")
            results["tx_features"] = False
        
        cls._models_loaded = True
        return results
    
    @classmethod
    def is_loaded(cls) -> bool:
        """Check if models have been loaded"""
        return cls._models_loaded
    
    @classmethod
    def get_fraud_model(cls) -> Optional[Any]:
        """Get the fraud detection model"""
        return cls._fraud_model
    
    @classmethod
    def get_fraud_features(cls) -> Optional[Any]:
        """Get fraud feature specifications"""
        return cls._fraud_features
    
    @classmethod
    def get_gas_model(cls) -> Optional[Any]:
        """Get the gas fee prediction model"""
        return cls._gas_model
    
    @classmethod
    def get_gas_features(cls) -> Optional[Any]:
        """Get gas feature specifications"""
        return cls._gas_features
    
    @classmethod
    def get_tx_classifier(cls) -> Optional[Any]:
        """Get the transaction classifier model"""
        return cls._tx_classifier
    
    @classmethod
    def get_tx_features(cls) -> Optional[Any]:
        """Get transaction feature specifications"""
        return cls._tx_features
    
    @classmethod
    def get_model_info(cls) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "models_loaded": cls._models_loaded,
            "fraud_model": {
                "loaded": cls._fraud_model is not None,
                "type": type(cls._fraud_model).__name__ if cls._fraud_model else None
            },
            "gas_model": {
                "loaded": cls._gas_model is not None,
                "type": type(cls._gas_model).__name__ if cls._gas_model else None
            },
            "tx_classifier": {
                "loaded": cls._tx_classifier is not None,
                "type": type(cls._tx_classifier).__name__ if cls._tx_classifier else None
            }
        }
