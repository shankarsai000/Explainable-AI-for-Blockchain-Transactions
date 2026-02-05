"""
Explanation Engine - Enhanced with accurate classification and calibrated explanations
Implements: Fix #1-6 for improved technical accuracy and human-readable output
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Current ETH price (should ideally be fetched from API)
ETH_PRICE_USD = 2500


class ExplanationEngine:
    """Generate natural language explanations for blockchain transactions"""
    
    # ==================== FIX #1: Classification Logic ====================
    
    def classify_transaction(self, decoded_tx: Dict) -> Dict[str, Any]:
        """
        Accurate transaction classification with contract detection and value tiers.
        
        Rules:
        1. ERC20 token contract interaction → Token Transfer
        2. No contract interaction → Native ETH Transfer
        3. Apply value tiers: Small (<1 ETH), Medium (1-10 ETH), High Value (>10 ETH)
        """
        value_eth = decoded_tx.get("value_eth", 0)
        is_token_transfer = decoded_tx.get("is_token_transfer", False)
        contract_interaction = decoded_tx.get("contract_interaction", False)
        method_name = decoded_tx.get("method_name", "")
        token_info = decoded_tx.get("token_info")
        to_address_info = decoded_tx.get("to_address_info")
        
        # Determine value tier
        if value_eth < 1:
            value_tier = "Small"
        elif value_eth <= 10:
            value_tier = "Medium"
        else:
            value_tier = "High Value"
        
        # Determine transaction type
        if is_token_transfer and token_info:
            # FIX #2: Use specific token name
            token_symbol = token_info.get("symbol", "Token")
            category = f"{token_symbol} Transfer"
            tx_type = "token_transfer"
            description = f"Transfer of {token_symbol} tokens"
        elif contract_interaction:
            # Check for specific contract interactions
            if method_name in ["swapExactETHForTokens", "swapExactTokensForTokens"]:
                category = "DEX Swap"
                tx_type = "dex_swap"
                description = "Token exchange on decentralized exchange"
            elif method_name in ["addLiquidity", "addLiquidityETH"]:
                category = "Liquidity Provision"
                tx_type = "liquidity"
                description = "Adding liquidity to a pool"
            elif method_name == "safeTransferFrom":
                category = "NFT Transfer"
                tx_type = "nft"
                description = "NFT token transfer"
            elif to_address_info and to_address_info.get("type") == "dex":
                category = "DEX Interaction"
                tx_type = "dex"
                description = f"Interaction with {to_address_info.get('name', 'DEX')}"
            elif to_address_info and to_address_info.get("type") == "nft":
                category = "NFT Transaction"
                tx_type = "nft"
                description = f"Interaction with {to_address_info.get('name', 'NFT platform')}"
            else:
                category = "Contract Interaction"
                tx_type = "contract"
                description = "Smart contract execution"
        else:
            # Native ETH transfer
            category = f"{value_tier} Native ETH Transfer"
            tx_type = "eth_transfer"
            description = f"Direct ETH transfer between addresses"
        
        # Add context about destination
        context_label = None
        if to_address_info:
            if to_address_info.get("type") == "exchange":
                context_label = f"Exchange deposit ({to_address_info.get('name', 'Exchange')})"
            elif to_address_info.get("type") == "dex":
                context_label = f"DEX interaction ({to_address_info.get('name', 'DEX')})"
        
        return {
            "category": category,
            "tx_type": tx_type,
            "value_tier": value_tier,
            "description": description,
            "context_label": context_label,
            "confidence": 0.92,
        }
    
    # ==================== FIX #3: Gas Explanation Calibration ====================
    
    def analyze_gas(self, decoded_tx: Dict, predicted_gas: float) -> Dict[str, Any]:
        """
        Calibrated gas analysis with tiered reasoning instead of raw percentages.
        
        Thresholds:
        - ±20% → Normal gas fee
        - +20-80% → Higher than average
        - +80%+ → Network congestion or priority execution
        """
        actual_gas = decoded_tx.get("gas_price_gwei", 0)
        gas_used = decoded_tx.get("gas_used", 21000)
        tx_fee_eth = decoded_tx.get("transaction_fee_eth", 0)
        
        # Calculate difference
        if predicted_gas > 0:
            diff_percent = ((actual_gas - predicted_gas) / predicted_gas) * 100
        else:
            diff_percent = 0
        
        # USD conversion
        fee_usd = tx_fee_eth * ETH_PRICE_USD
        
        # Tiered gas explanation (FIX #3)
        if abs(diff_percent) <= 20:
            efficiency = "NORMAL"
            explanation = "Gas fees were within normal range for network conditions."
            status = "optimal"
        elif diff_percent > 20 and diff_percent <= 80:
            efficiency = "ABOVE_AVERAGE"
            explanation = "Gas fees were higher than average, likely due to moderate network activity."
            status = "elevated"
        elif diff_percent > 80:
            efficiency = "CONGESTED"
            explanation = "Gas fees were significantly higher than predicted, indicating temporary network congestion or priority execution."
            status = "high"
        elif diff_percent < -20:
            efficiency = "EXCELLENT"
            explanation = "Gas fees were lower than predicted - excellent timing!"
            status = "low"
        else:
            efficiency = "NORMAL"
            explanation = "Gas fees were within expected parameters."
            status = "normal"
        
        return {
            "predicted_gas_gwei": round(predicted_gas, 2),
            "actual_gas_gwei": round(actual_gas, 2),
            "difference_percent": round(diff_percent, 1),
            "efficiency": efficiency,
            "explanation": explanation,
            "status": status,
            "fee_eth": round(tx_fee_eth, 6),
            "fee_usd": round(fee_usd, 2),
            "gas_used": gas_used,
        }
    
    # ==================== FIX #4: Fraud Explanation ====================
    
    def generate_fraud_explanation(self, fraud_analysis: Dict) -> str:
        """
        Always generate a risk statement, even when safe.
        """
        risk_level = fraud_analysis.get("risk_level", "UNKNOWN")
        risk_score = fraud_analysis.get("risk_score", 0)
        
        if risk_level == "LOW" or risk_score < 0.3:
            return "No suspicious wallet behavior detected."
        elif risk_level == "MEDIUM" or risk_score < 0.6:
            return "Transaction shows mild anomaly patterns. Exercise normal caution."
        elif risk_level == "HIGH" or risk_score < 0.8:
            return "Wallet behavior shows concerning patterns. Verify recipient before proceeding."
        else:
            return "⚠️ Wallet behavior matches known phishing or scam activity patterns."
    
    # ==================== FIX #5: Contextual Interpretation ====================
    
    def generate_context_insight(self, decoded_tx: Dict, classification: Dict) -> str:
        """
        Add human-readable context insights based on transaction patterns.
        """
        value_eth = decoded_tx.get("value_eth", 0)
        to_address_info = decoded_tx.get("to_address_info")
        from_address_info = decoded_tx.get("from_address_info")
        tx_type = classification.get("tx_type", "unknown")
        token_info = decoded_tx.get("token_info")
        
        # Exchange interactions
        if to_address_info and to_address_info.get("type") == "exchange":
            exchange_name = to_address_info.get("name", "exchange")
            if value_eth > 10:
                return f"This transaction resembles a large exchange deposit to {exchange_name}, possibly for trading or liquidation."
            else:
                return f"This transaction appears to be a standard deposit to {exchange_name}."
        
        # Whale detection
        if value_eth > 100:
            return "This is a whale-sized transfer, potentially representing institutional movement or large asset reallocation."
        elif value_eth > 50:
            return "This is a significant transfer that may represent portfolio rebalancing or large-scale trading activity."
        
        # DEX interactions
        if tx_type == "dex_swap":
            return "This transaction is a token swap on a decentralized exchange, exchanging one asset for another."
        
        if tx_type == "liquidity":
            return "This transaction adds liquidity to a trading pool, enabling market making and earning fees."
        
        # Token transfers
        if tx_type == "token_transfer" and token_info:
            symbol = token_info.get("symbol", "tokens")
            if symbol in ["USDT", "USDC", "DAI"]:
                return f"This is a stablecoin transfer ({symbol}), commonly used for payments or trading settlements."
            return f"This is a {symbol} token transfer between addresses."
        
        # NFT transactions
        if tx_type == "nft":
            return "This transaction involves NFT (digital collectible) movement, possibly a purchase, sale, or transfer."
        
        # Default for ETH transfers
        if tx_type == "eth_transfer":
            if value_eth > 10:
                return "This transaction resembles a large asset movement or exchange deposit."
            elif value_eth < 0.1:
                return "This is a small ETH transfer, possibly for testing or micro-payments."
            else:
                return "This is a standard ETH transfer between addresses."
        
        return "Transaction context could not be fully determined."
    
    # ==================== FIX #6: Standardized Explanation Format ====================
    
    def generate_explanation(
        self, decoded_tx: Dict, fraud_analysis: Dict,
        gas_analysis: Dict, classification: Dict, language: str = "en"
    ) -> Dict[str, str]:
        """Generate complete standardized explanation (Fix #6 format)"""
        summary = self._generate_summary(decoded_tx, classification)
        full_text = self._generate_full_explanation(
            decoded_tx, fraud_analysis, gas_analysis, classification
        )
        return {"summary": summary, "full_text": full_text}
    
    def _generate_summary(self, decoded_tx: Dict, classification: Dict) -> str:
        """Generate one-line summary with accurate classification"""
        value = decoded_tx.get("value_eth", 0)
        token_info = decoded_tx.get("token_info")
        token_amount = decoded_tx.get("token_amount")
        category = classification.get("category", "Transaction")
        status = decoded_tx.get("status", "Success")
        
        # Token transfer summary
        if token_info and token_amount:
            symbol = token_info.get("symbol", "tokens")
            return f"{status}: {token_amount:,.2f} {symbol} transferred"
        
        # ETH transfer summary
        if value > 0:
            return f"{status}: {value:.4f} ETH - {category}"
        
        return f"{status}: {category}"
    
    def _generate_full_explanation(
        self, decoded_tx: Dict, fraud_analysis: Dict,
        gas_analysis: Dict, classification: Dict
    ) -> str:
        """
        Generate detailed explanation in standardized format (Fix #6):
        1. Transaction summary
        2. Classification
        3. Gas analysis
        4. Fraud risk
        5. Context insight
        """
        lines = []
        
        # 1. Transaction Summary
        value = decoded_tx.get("value_eth", 0)
        token_info = decoded_tx.get("token_info")
        token_amount = decoded_tx.get("token_amount")
        from_addr = self._format_address(decoded_tx.get("from_address", "Unknown"))
        to_addr = self._format_address(decoded_tx.get("to_address", "Unknown"))
        to_addr_info = decoded_tx.get("to_address_info")
        
        # Use known name if available
        if to_addr_info:
            to_display = to_addr_info.get("name", to_addr)
        else:
            to_display = to_addr
        
        if token_info and token_amount:
            symbol = token_info.get("symbol", "tokens")
            lines.append(f"You transferred {token_amount:,.2f} {symbol} from {from_addr} to {to_display}.")
        elif value > 0:
            lines.append(f"You transferred {value:.4f} ETH from {from_addr} to {to_display}.")
        else:
            lines.append(f"You executed a contract interaction from {from_addr} to {to_display}.")
        
        lines.append("")  # Empty line for formatting
        
        # 2. Classification
        category = classification.get("category", "Unknown")
        lines.append(f"This is classified as a {category}.")
        
        lines.append("")
        
        # 3. Gas Analysis (Fix #3 - calibrated)
        gas_explanation = gas_analysis.get("explanation", "Gas fees were within normal range.")
        fee_usd = gas_analysis.get("fee_usd", 0)
        lines.append(f"{gas_explanation} (Fee: ${fee_usd:.2f} USD)")
        
        lines.append("")
        
        # 4. Fraud Risk (Fix #4 - always include)
        fraud_explanation = self.generate_fraud_explanation(fraud_analysis)
        lines.append(fraud_explanation)
        
        lines.append("")
        
        # 5. Context Insight (Fix #5)
        context = self.generate_context_insight(decoded_tx, classification)
        lines.append(context)
        
        return "\n".join(lines)
    
    def _format_address(self, address: str, length: int = 8) -> str:
        """Format address for display"""
        if not address or len(address) < 15:
            return address or "Unknown"
        return f"{address[:6]}...{address[-4:]}"
    
    def generate_quick_summary(self, decoded_tx: Dict) -> str:
        """Generate quick one-line summary with token detection"""
        value = decoded_tx.get("value_eth", 0)
        status = decoded_tx.get("status", "Success")
        token_info = decoded_tx.get("token_info")
        token_amount = decoded_tx.get("token_amount")
        
        if token_info and token_amount:
            symbol = token_info.get("symbol", "tokens")
            return f"{status}: Transferred {token_amount:,.2f} {symbol}"
        
        if decoded_tx.get("contract_interaction"):
            method = decoded_tx.get("method_name", "Unknown")
            return f"{status}: Contract call ({method}) with {value:.4f} ETH"
        
        return f"{status}: Transferred {value:.4f} ETH"
    
    def generate_visualization_data(
        self, decoded_tx: Dict, fraud_analysis: Dict,
        gas_analysis: Dict, classification: Dict
    ) -> Dict[str, Any]:
        """Generate data for frontend visualizations"""
        return {
            "gas_chart": {
                "predicted": gas_analysis.get("predicted_gas_gwei", 0),
                "actual": gas_analysis.get("actual_gas_gwei", 0),
                "average": (gas_analysis.get("predicted_gas_gwei", 0) + gas_analysis.get("actual_gas_gwei", 0)) / 2,
                "fee_usd": gas_analysis.get("fee_usd", 0),
            },
            "fraud_gauge": {
                "score": fraud_analysis.get("risk_score", 0),
                "level": fraud_analysis.get("risk_level", "UNKNOWN"),
                "max_score": 1.0,
                "explanation": self.generate_fraud_explanation(fraud_analysis),
            },
            "value_scale": {
                "value_eth": decoded_tx.get("value_eth", 0),
                "value_usd": decoded_tx.get("value_eth", 0) * ETH_PRICE_USD,
                "fee_eth": decoded_tx.get("transaction_fee_eth", 0),
                "fee_usd": decoded_tx.get("transaction_fee_eth", 0) * ETH_PRICE_USD,
                "token_amount": decoded_tx.get("token_amount"),
                "token_symbol": decoded_tx.get("token_info", {}).get("symbol") if decoded_tx.get("token_info") else None,
            },
            "flow_diagram": {
                "from": decoded_tx.get("from_address", ""),
                "to": decoded_tx.get("to_address", ""),
                "to_name": decoded_tx.get("to_address_info", {}).get("name") if decoded_tx.get("to_address_info") else None,
                "value": decoded_tx.get("value_eth", 0),
                "is_contract": decoded_tx.get("contract_interaction", False),
                "is_token": decoded_tx.get("is_token_transfer", False),
            },
        }
    
    def generate_recommendations(
        self, fraud_analysis: Dict, gas_analysis: Dict, classification: Dict
    ) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        risk_level = fraud_analysis.get("risk_level", "UNKNOWN")
        if risk_level == "HIGH":
            recs.append("Consider verifying the recipient address before future transactions.")
            recs.append("Check the recipient's transaction history on blockchain explorers.")
        elif risk_level == "CRITICAL":
            recs.append("⚠️ Do not proceed with similar transactions until verified.")
            recs.append("Report suspicious addresses to community blacklists.")
        
        efficiency = gas_analysis.get("efficiency", "NORMAL")
        if efficiency in ["CONGESTED", "ABOVE_AVERAGE"]:
            recs.append("Consider waiting for lower gas periods (UTC 2-6 AM) for non-urgent transactions.")
            recs.append("Use gas tracking tools to identify optimal transaction times.")
        
        if not recs:
            recs.append("Transaction completed successfully. No immediate action required.")
        
        return recs
    
    def build_sections(
        self, decoded_tx: Dict, fraud_analysis: Dict,
        gas_analysis: Dict, classification: Dict
    ) -> List[Dict[str, str]]:
        """Build explanation sections for UI with enhanced data"""
        value = decoded_tx.get("value_eth", 0)
        token_info = decoded_tx.get("token_info")
        token_amount = decoded_tx.get("token_amount")
        
        # Value display
        if token_info and token_amount:
            value_display = f"{token_amount:,.2f} {token_info.get('symbol', 'tokens')}"
        else:
            value_display = f"{value:.4f} ETH"
        
        return [
            {
                "title": "Transaction Overview",
                "content": value_display,
                "importance": "high",
                "icon": "💰",
            },
            {
                "title": "Classification",
                "content": classification.get("category", "Unknown"),
                "importance": "medium",
                "icon": "🏷️",
            },
            {
                "title": "Gas Analysis",
                "content": f"${gas_analysis.get('fee_usd', 0):.2f} ({gas_analysis.get('efficiency', 'Normal')})",
                "importance": "medium",
                "icon": "⛽",
            },
            {
                "title": "Security",
                "content": self.generate_fraud_explanation(fraud_analysis),
                "importance": "high" if fraud_analysis.get("risk_level") in ["HIGH", "CRITICAL"] else "low",
                "icon": "🛡️",
            },
        ]
