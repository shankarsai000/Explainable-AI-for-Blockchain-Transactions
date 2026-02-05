"""
Transaction decoding and fetching routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import re

from services.blockchain_service import BlockchainService
from services.feature_extractor import FeatureExtractor


router = APIRouter()


class TransactionHashRequest(BaseModel):
    """Request model for transaction hash input"""
    tx_hash: str = Field(..., description="Ethereum transaction hash", 
                         pattern="^0x[a-fA-F0-9]{64}$")


class DecodedTransaction(BaseModel):
    """Response model for decoded transaction"""
    hash: str
    block_number: int
    timestamp: Optional[int]
    from_address: str
    to_address: Optional[str]
    value_wei: str
    value_eth: float
    gas_used: int
    gas_price_gwei: float
    gas_limit: int
    transaction_fee_eth: float
    nonce: int
    input_data: str
    status: str
    contract_interaction: bool
    method_id: Optional[str]
    method_name: Optional[str]


@router.post("/decode_tx", response_model=DecodedTransaction)
async def decode_transaction(request: TransactionHashRequest):
    """
    Decode a blockchain transaction from its hash.
    
    Fetches transaction data from the blockchain and decodes:
    - Sender and receiver addresses
    - Value transferred
    - Gas usage and fees
    - Contract interaction details
    """
    try:
        # Validate hash format
        if not re.match(r'^0x[a-fA-F0-9]{64}$', request.tx_hash):
            raise HTTPException(status_code=400, detail="Invalid transaction hash format")
        
        # Fetch transaction from blockchain
        blockchain_service = BlockchainService()
        tx_data = await blockchain_service.get_transaction(request.tx_hash)
        
        if not tx_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Get transaction receipt for additional details
        receipt = await blockchain_service.get_transaction_receipt(request.tx_hash)
        
        # Decode the transaction
        decoded = await blockchain_service.decode_transaction(tx_data, receipt)
        
        return decoded
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding transaction: {str(e)}")


@router.get("/tx/{tx_hash}/features")
async def get_transaction_features(tx_hash: str):
    """
    Extract ML features from a transaction for prediction models
    """
    try:
        blockchain_service = BlockchainService()
        tx_data = await blockchain_service.get_transaction(tx_hash)
        
        if not tx_data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        receipt = await blockchain_service.get_transaction_receipt(tx_hash)
        
        # Extract features for ML models
        feature_extractor = FeatureExtractor()
        features = feature_extractor.extract_all_features(tx_data, receipt)
        
        return {
            "tx_hash": tx_hash,
            "features": features
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting features: {str(e)}")


@router.get("/address/{address}/stats")
async def get_address_stats(address: str):
    """
    Get historical statistics for an address (for fraud detection)
    """
    try:
        blockchain_service = BlockchainService()
        stats = await blockchain_service.get_address_stats(address)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching address stats: {str(e)}")
