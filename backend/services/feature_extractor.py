"""Feature Extractor Service - Prepares features for ML models"""

from typing import Dict, Any, List, Optional
import numpy as np


class FeatureExtractor:
    """Extract and prepare features for ML predictions"""
    
    def extract_all_features(self, tx_data: Dict, receipt: Optional[Dict] = None) -> Dict:
        """Extract all feature sets from transaction data"""
        return {
            "wallet_features": self._extract_wallet_features(tx_data),
            "gas_features": self._extract_gas_features(tx_data, receipt),
            "tx_features": self._extract_tx_features(tx_data, receipt),
        }
    
    def _extract_wallet_features(self, tx_data: Dict) -> Dict:
        """Extract wallet-related features for fraud detection"""
        value = int(tx_data.get("value", 0))
        return {
            "transaction_count": 50, "total_value_sent": float(value) / 1e18,
            "total_value_received": float(value) / 1e18 * 0.8,
            "unique_addresses_interacted": 25, "avg_transaction_value": float(value) / 1e18,
            "max_transaction_value": float(value) / 1e18 * 2,
            "min_transaction_value": float(value) / 1e18 * 0.1,
            "avg_gas_price": 30.0, "contract_creation_count": 0,
            "failed_transaction_ratio": 0.02, "time_between_txs_avg": 3600,
        }
    
    def _extract_gas_features(self, tx_data: Dict, receipt: Optional[Dict]) -> Dict:
        """Extract gas-related features"""
        from web3 import Web3
        w3 = Web3()
        gas_price = int(tx_data.get("gasPrice", 0))
        value = int(tx_data.get("value", 0))
        input_data = tx_data.get("input", "0x")
        if isinstance(input_data, bytes):
            input_data = input_data.hex()
        
        return {
            "value_eth": float(w3.from_wei(value, 'ether')),
            "gas_limit": int(tx_data.get("gas", 21000)),
            "is_contract_call": len(input_data) > 2,
            "input_data_size": len(input_data) // 2,
            "network_congestion": 0.5,
            "time_of_day": 12, "day_of_week": 3,
        }
    
    def _extract_tx_features(self, tx_data: Dict, receipt: Optional[Dict]) -> Dict:
        """Extract transaction classification features"""
        from web3 import Web3
        w3 = Web3()
        value = int(tx_data.get("value", 0))
        input_data = tx_data.get("input", "0x")
        if isinstance(input_data, bytes):
            input_data = input_data.hex()
        gas_used = int(receipt.get("gasUsed", 21000)) if receipt else 21000
        
        return {
            "value_eth": float(w3.from_wei(value, 'ether')),
            "gas_used": gas_used, "input_data_length": len(input_data),
            "to_address_type": "contract" if len(input_data) > 2 else "eoa",
            "from_address_type": "eoa",
            "method_id": input_data[:10] if len(input_data) >= 10 else None,
        }
    
    def prepare_fraud_features(self, data: Dict, features_info: Any) -> List[float]:
        """Prepare features array for fraud model"""
        feature_order = [
            "transaction_count", "total_value_sent", "total_value_received",
            "unique_addresses_interacted", "avg_transaction_value",
            "max_transaction_value", "min_transaction_value", "avg_gas_price",
            "contract_creation_count", "failed_transaction_ratio", "time_between_txs_avg",
        ]
        return [float(data.get(f, 0)) for f in feature_order]
    
    def prepare_gas_features(self, data: Dict, features_info: Any) -> List[float]:
        """Prepare features array for gas model"""
        return [
            float(data.get("value_eth", 0)), float(data.get("gas_limit", 21000)),
            1.0 if data.get("is_contract_call") else 0.0,
            float(data.get("input_data_size", 0)), float(data.get("network_congestion", 0.5)),
            float(data.get("time_of_day", 12)), float(data.get("day_of_week", 3)),
        ]
    
    def prepare_tx_features(self, data: Dict, features_info: Any) -> List[float]:
        """Prepare features array for transaction classifier"""
        type_map = {"eoa": 0, "contract": 1, "exchange": 2, "defi": 3}
        return [
            float(data.get("value_eth", 0)), float(data.get("gas_used", 21000)),
            float(data.get("input_data_length", 0)),
            float(type_map.get(data.get("to_address_type", "eoa"), 0)),
            float(type_map.get(data.get("from_address_type", "eoa"), 0)),
        ]
    
    def identify_risk_factors(self, data: Dict) -> List[str]:
        """Identify risk factors from wallet data"""
        risk_factors = []
        if data.get("failed_transaction_ratio", 0) > 0.1:
            risk_factors.append("High failed transaction ratio")
        if data.get("transaction_count", 0) < 5:
            risk_factors.append("New wallet with limited history")
        if data.get("max_transaction_value", 0) > 100:
            risk_factors.append("Large value transactions detected")
        if data.get("time_between_txs_avg", 0) < 60:
            risk_factors.append("Rapid transaction frequency")
        if not risk_factors:
            risk_factors.append("No significant risk factors identified")
        return risk_factors
