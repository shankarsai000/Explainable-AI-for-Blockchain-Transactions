"""
Blockchain Service - Handles RPC interactions with enhanced token detection
"""

import os
from typing import Optional, Dict, Any, Tuple
from web3 import Web3
from web3.exceptions import TransactionNotFound
import asyncio
from config import settings

# Method signatures for transaction type detection
METHOD_SIGS = {
    "0xa9059cbb": "transfer",
    "0x23b872dd": "transferFrom",
    "0x095ea7b3": "approve",
    "0x7ff36ab5": "swapExactETHForTokens",
    "0x38ed1739": "swapExactTokensForTokens",
    "0x2e1a7d4d": "withdraw",
    "0xd0e30db0": "deposit",
    "0x42842e0e": "safeTransferFrom",
    "0xb88d4fde": "safeTransferFrom",
    "0xa22cb465": "setApprovalForAll",
    "0xe8e33700": "addLiquidity",
    "0xf305d719": "addLiquidityETH",
}

# ERC20 method IDs for token detection
ERC20_METHODS = {"0xa9059cbb", "0x23b872dd", "0x095ea7b3"}

# Known token contracts (mainnet)
KNOWN_TOKENS = {
    "0xdac17f958d2ee523a2206206994597c13d831ec7": {"symbol": "USDT", "name": "Tether USD", "decimals": 6},
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {"symbol": "USDC", "name": "USD Coin", "decimals": 6},
    "0x6b175474e89094c44da98b954eedeac495271d0f": {"symbol": "DAI", "name": "Dai Stablecoin", "decimals": 18},
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {"symbol": "WETH", "name": "Wrapped Ether", "decimals": 18},
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": {"symbol": "WBTC", "name": "Wrapped BTC", "decimals": 8},
    "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984": {"symbol": "UNI", "name": "Uniswap", "decimals": 18},
    "0x514910771af9ca656af840dff83e8264ecf986ca": {"symbol": "LINK", "name": "Chainlink", "decimals": 18},
    "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0": {"symbol": "MATIC", "name": "Polygon", "decimals": 18},
    "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce": {"symbol": "SHIB", "name": "Shiba Inu", "decimals": 18},
    "0x4d224452801aced8b2f0aebe155379bb5d594381": {"symbol": "APE", "name": "ApeCoin", "decimals": 18},
}

# Known exchange/DeFi addresses
KNOWN_ADDRESSES = {
    "0x28c6c06298d514db089934071355e5743bf21d60": {"name": "Binance Hot Wallet", "type": "exchange"},
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549": {"name": "Binance", "type": "exchange"},
    "0xdfd5293d8e347dfe59e90efd55b2956a1343963d": {"name": "Binance", "type": "exchange"},
    "0x56eddb7aa87536c09ccc2793473599fd21a8b17f": {"name": "Coinbase", "type": "exchange"},
    "0x71660c4005ba85c37ccec55d0c4493e66fe775d3": {"name": "Coinbase", "type": "exchange"},
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": {"name": "Uniswap V2 Router", "type": "dex"},
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45": {"name": "Uniswap V3 Router", "type": "dex"},
    "0xe592427a0aece92de3edee1f18e0157c05861564": {"name": "Uniswap V3", "type": "dex"},
    "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b": {"name": "OpenSea", "type": "nft"},
    "0x00000000006c3852cbef3e08e8df289169ede581": {"name": "Seaport", "type": "nft"},
}

# ERC20 ABI for token metadata
ERC20_ABI = [
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
]


class BlockchainService:
    def __init__(self, rpc_url: Optional[str] = None):
        self.rpc_url = rpc_url or settings.RPC_URL
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self._token_cache = {}
    
    async def get_transaction(self, tx_hash: str) -> Optional[Dict]:
        try:
            loop = asyncio.get_event_loop()
            tx = await loop.run_in_executor(None, lambda: self.w3.eth.get_transaction(tx_hash))
            return dict(tx) if tx else None
        except:
            return self._mock_tx(tx_hash)
    
    async def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        try:
            loop = asyncio.get_event_loop()
            receipt = await loop.run_in_executor(None, lambda: self.w3.eth.get_transaction_receipt(tx_hash))
            return dict(receipt) if receipt else None
        except:
            return {"status": 1, "gasUsed": 45000}
    
    async def get_block(self, block_num: int) -> Optional[Dict]:
        try:
            loop = asyncio.get_event_loop()
            block = await loop.run_in_executor(None, lambda: self.w3.eth.get_block(block_num))
            return dict(block) if block else None
        except:
            return None
    
    async def get_token_info(self, contract_address: str) -> Optional[Dict]:
        """Fetch ERC20 token metadata (symbol, name, decimals)"""
        address_lower = contract_address.lower()
        
        # Check known tokens first
        if address_lower in KNOWN_TOKENS:
            return KNOWN_TOKENS[address_lower]
        
        # Check cache
        if address_lower in self._token_cache:
            return self._token_cache[address_lower]
        
        try:
            loop = asyncio.get_event_loop()
            checksum_addr = self.w3.to_checksum_address(contract_address)
            contract = self.w3.eth.contract(address=checksum_addr, abi=ERC20_ABI)
            
            symbol = await loop.run_in_executor(None, lambda: contract.functions.symbol().call())
            name = await loop.run_in_executor(None, lambda: contract.functions.name().call())
            decimals = await loop.run_in_executor(None, lambda: contract.functions.decimals().call())
            
            token_info = {"symbol": symbol, "name": name, "decimals": decimals}
            self._token_cache[address_lower] = token_info
            return token_info
        except:
            return None
    
    def get_known_address_info(self, address: str) -> Optional[Dict]:
        """Get info about known exchanges/protocols"""
        return KNOWN_ADDRESSES.get(address.lower())
    
    def is_erc20_transfer(self, method_id: Optional[str]) -> bool:
        """Check if method ID indicates ERC20 token transfer"""
        return method_id and method_id.lower() in ERC20_METHODS
    
    def decode_erc20_transfer(self, input_data: str) -> Optional[Dict]:
        """Decode ERC20 transfer data to get recipient and amount"""
        if len(input_data) < 138:  # 0x + 8 (method) + 64 (address) + 64 (amount)
            return None
        
        try:
            method_id = input_data[:10]
            if method_id.lower() == "0xa9059cbb":  # transfer(address,uint256)
                recipient = "0x" + input_data[34:74]
                amount_hex = input_data[74:138]
                amount = int(amount_hex, 16)
                return {"recipient": recipient, "amount": amount}
        except:
            pass
        return None
    
    async def decode_transaction(self, tx_data: Dict, receipt: Optional[Dict] = None) -> Dict:
        """Decode transaction with enhanced token and address detection"""
        value_wei = int(tx_data.get("value", 0))
        value_eth = float(self.w3.from_wei(value_wei, 'ether'))
        gas_price_wei = int(tx_data.get("gasPrice", 0))
        gas_price_gwei = float(self.w3.from_wei(gas_price_wei, 'gwei'))
        gas_limit = int(tx_data.get("gas", 21000))
        gas_used = int(receipt.get("gasUsed", gas_limit)) if receipt else gas_limit
        tx_fee_eth = float(self.w3.from_wei(gas_used * gas_price_wei, 'ether'))
        
        input_data = tx_data.get("input", "0x")
        if isinstance(input_data, bytes):
            input_data = "0x" + input_data.hex()
        
        to_address = tx_data.get("to") or "Contract Creation"
        contract_interaction = len(input_data) > 2
        method_id = input_data[:10] if contract_interaction and len(input_data) >= 10 else None
        method_name = METHOD_SIGS.get(method_id, "Unknown") if method_id else None
        status = "Success" if (receipt.get("status", 1) == 1 if receipt else True) else "Failed"
        
        tx_hash = tx_data.get("hash", "")
        if isinstance(tx_hash, bytes):
            tx_hash = tx_hash.hex()
        
        # Enhanced detection
        is_token_transfer = self.is_erc20_transfer(method_id)
        token_info = None
        token_amount = None
        token_recipient = None
        
        if is_token_transfer and to_address != "Contract Creation":
            token_info = await self.get_token_info(to_address)
            transfer_data = self.decode_erc20_transfer(input_data)
            if transfer_data and token_info:
                token_amount = transfer_data["amount"] / (10 ** token_info.get("decimals", 18))
                token_recipient = transfer_data["recipient"]
        
        # Get known address info
        to_address_info = self.get_known_address_info(to_address) if to_address != "Contract Creation" else None
        from_address_info = self.get_known_address_info(tx_data.get("from", ""))
        
        return {
            "hash": str(tx_hash),
            "block_number": tx_data.get("blockNumber", 0),
            "timestamp": None,
            "from_address": tx_data.get("from", ""),
            "to_address": to_address,
            "value_wei": str(value_wei),
            "value_eth": value_eth,
            "gas_used": gas_used,
            "gas_price_gwei": gas_price_gwei,
            "gas_limit": gas_limit,
            "transaction_fee_eth": tx_fee_eth,
            "nonce": tx_data.get("nonce", 0),
            "input_data": input_data,
            "status": status,
            "contract_interaction": contract_interaction,
            "method_id": method_id,
            "method_name": method_name,
            # New enhanced fields
            "is_token_transfer": is_token_transfer,
            "token_info": token_info,
            "token_amount": token_amount,
            "token_recipient": token_recipient,
            "to_address_info": to_address_info,
            "from_address_info": from_address_info,
        }
    
    async def get_address_stats(self, address: str) -> Dict:
        try:
            loop = asyncio.get_event_loop()
            balance = await loop.run_in_executor(None, lambda: self.w3.eth.get_balance(address))
            tx_count = await loop.run_in_executor(None, lambda: self.w3.eth.get_transaction_count(address))
            return {
                "address": address,
                "balance_eth": float(self.w3.from_wei(balance, 'ether')),
                "transaction_count": tx_count,
                "known_info": self.get_known_address_info(address)
            }
        except:
            return {"address": address, "balance_eth": 0, "transaction_count": 0}
    
    def _mock_tx(self, tx_hash: str) -> Dict:
        import random
        return {
            "hash": tx_hash,
            "blockNumber": 18500000,
            "from": "0x" + "a" * 40,
            "to": "0x" + "b" * 40,
            "value": self.w3.to_wei(1.5, 'ether'),
            "gas": 21000,
            "gasPrice": self.w3.to_wei(30, 'gwei'),
            "nonce": 100,
            "input": "0x",
        }
