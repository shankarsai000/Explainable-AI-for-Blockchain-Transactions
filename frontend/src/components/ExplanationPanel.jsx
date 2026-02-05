export default function ExplanationPanel({ explanation, summary, sections, transaction, contextInsight, classification }) {
    const formatAddress = (addr) => {
        if (!addr || addr.length < 15) return addr
        return `${addr.slice(0, 8)}...${addr.slice(-6)}`
    }

    // Get token info if available
    const tokenInfo = transaction?.token_info
    const tokenAmount = transaction?.token_amount
    const toAddressInfo = transaction?.to_address_info

    // Display value (token or ETH)
    const getValueDisplay = () => {
        if (tokenInfo && tokenAmount) {
            return { value: tokenAmount.toLocaleString(undefined, { maximumFractionDigits: 2 }), unit: tokenInfo.symbol }
        }
        return { value: transaction?.value_eth?.toFixed(4) || '0', unit: 'ETH' }
    }

    const valueDisplay = getValueDisplay()

    return (
        <div className="glass rounded-2xl overflow-hidden card-hover">
            {/* Header */}
            <div className="bg-gradient-to-r from-primary-600/20 to-accent-600/20 px-6 py-4 border-b border-white/5">
                <div className="flex items-center justify-between flex-wrap gap-2">
                    <h2 className="text-xl font-bold text-white flex items-center gap-2">
                        <span>📊</span> Transaction Analysis
                    </h2>
                    <div className="flex items-center gap-2">
                        {classification?.category && (
                            <span className="badge badge-info">
                                {classification.category}
                            </span>
                        )}
                        <span className={`badge ${transaction?.status === 'Success' ? 'badge-success' : 'badge-danger'}`}>
                            {transaction?.status || 'Unknown'}
                        </span>
                    </div>
                </div>
                <p className="text-gray-400 text-sm mt-1">{summary}</p>
            </div>

            {/* Transaction Details */}
            <div className="p-6 border-b border-white/5">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="glass-light rounded-xl p-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Value</p>
                        <p className="text-2xl font-bold text-white">{valueDisplay.value}</p>
                        <p className="text-sm text-gray-400">{valueDisplay.unit}</p>
                    </div>

                    <div className="glass-light rounded-xl p-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Gas Used</p>
                        <p className="text-2xl font-bold text-white">{transaction?.gas_used?.toLocaleString() || 0}</p>
                        <p className="text-sm text-gray-400">units</p>
                    </div>

                    <div className="glass-light rounded-xl p-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Gas Price</p>
                        <p className="text-2xl font-bold text-white">{transaction?.gas_price_gwei?.toFixed(2) || 0}</p>
                        <p className="text-sm text-gray-400">gwei</p>
                    </div>

                    <div className="glass-light rounded-xl p-4">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">Fee</p>
                        <p className="text-2xl font-bold text-white">{transaction?.transaction_fee_eth?.toFixed(6) || 0}</p>
                        <p className="text-sm text-gray-400">ETH</p>
                    </div>
                </div>
            </div>

            {/* Addresses */}
            <div className="p-6 border-b border-white/5">
                <div className="flex flex-col sm:flex-row items-center gap-4">
                    <div className="flex-1 text-center sm:text-left">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">From</p>
                        <p className="text-sm font-mono text-gray-300">{formatAddress(transaction?.from_address)}</p>
                        {transaction?.from_address_info && (
                            <p className="text-xs text-primary-400 mt-1">{transaction.from_address_info.name}</p>
                        )}
                    </div>

                    <div className="flex flex-col items-center">
                        <div className="text-primary-400 text-2xl">→</div>
                        {tokenInfo && (
                            <span className="text-xs text-accent-400 mt-1">{tokenInfo.symbol}</span>
                        )}
                    </div>

                    <div className="flex-1 text-center sm:text-right">
                        <p className="text-xs text-gray-500 uppercase tracking-wide mb-1">To</p>
                        <p className="text-sm font-mono text-gray-300">
                            {toAddressInfo?.name || formatAddress(transaction?.to_address)}
                        </p>
                        {toAddressInfo && (
                            <p className="text-xs text-accent-400 mt-1">{toAddressInfo.type}</p>
                        )}
                    </div>
                </div>
            </div>

            {/* Natural Language Explanation */}
            <div className="p-6 border-b border-white/5">
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                    <span>💬</span> AI Explanation
                </h3>
                <div className="text-gray-300 leading-relaxed bg-dark-700/50 rounded-xl p-4 whitespace-pre-line">
                    {explanation}
                </div>
            </div>

            {/* Context Insight (Fix #5) */}
            {contextInsight && (
                <div className="px-6 pb-4">
                    <div className="flex items-start gap-3 bg-gradient-to-r from-primary-500/10 to-accent-500/10 rounded-xl p-4 border border-primary-500/20">
                        <span className="text-xl">💡</span>
                        <div>
                            <p className="text-sm font-semibold text-primary-300 mb-1">Context Insight</p>
                            <p className="text-sm text-gray-300">{contextInsight}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Quick Sections */}
            {sections && sections.length > 0 && (
                <div className="px-6 pb-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {sections.map((section, idx) => (
                            <div
                                key={idx}
                                className={`glass-light rounded-xl p-3 text-center
                  ${section.importance === 'high' ? 'ring-1 ring-primary-500/30' : ''}`}
                            >
                                <span className="text-2xl">{section.icon}</span>
                                <p className="text-xs text-gray-500 mt-1">{section.title}</p>
                                <p className="text-sm font-medium text-white truncate" title={section.content}>
                                    {section.content}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
