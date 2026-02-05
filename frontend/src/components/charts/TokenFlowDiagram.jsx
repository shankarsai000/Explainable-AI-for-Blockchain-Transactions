export default function TokenFlowDiagram({ from, to, value, isContract, isToken, tokenSymbol, tokenAmount, toName }) {
    const formatAddress = (addr) => {
        if (!addr || addr.length < 15) return addr || 'Unknown'
        return `${addr.slice(0, 6)}...${addr.slice(-4)}`
    }

    // Determine what to display
    const displayValue = isToken && tokenAmount ? `${tokenAmount.toLocaleString(undefined, { maximumFractionDigits: 2 })} ${tokenSymbol}` : `${value.toFixed(4)} ETH`
    const usdValue = isToken ? null : value * 2500 // Only show USD for ETH transfers

    return (
        <div className="glass rounded-2xl p-6 card-hover">
            <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <span>🔄</span> Transaction Flow
            </h3>

            {/* Flow Visualization */}
            <div className="flex items-center justify-between gap-4">
                {/* From Address */}
                <div className="flex-1 max-w-[140px]">
                    <div className="glass-light rounded-xl p-4 text-center relative overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent" />
                        <div className="relative">
                            <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                                <span className="text-xl">👤</span>
                            </div>
                            <p className="text-xs text-gray-500 mb-1">Sender</p>
                            <p className="text-xs font-mono text-gray-300 truncate">
                                {formatAddress(from)}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Flow Arrow */}
                <div className="flex-1 flex flex-col items-center">
                    {/* Value Badge */}
                    <div className={`mb-2 px-4 py-2 rounded-full shadow-lg ${isToken ? 'bg-gradient-to-r from-accent-500 to-pink-500' : 'bg-gradient-to-r from-primary-500 to-accent-500'}`}>
                        <p className="text-white font-bold text-sm">{displayValue}</p>
                    </div>

                    {/* Arrow */}
                    <div className="relative w-full flex items-center">
                        <div className={`flex-1 h-0.5 ${isToken ? 'bg-gradient-to-r from-accent-500 via-pink-500 to-rose-500' : 'bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500'}`} />
                        <div className={`w-0 h-0 border-t-4 border-b-4 border-l-8 border-transparent ${isToken ? 'border-l-rose-500' : 'border-l-pink-500'}`} />
                    </div>

                    {/* Token indicator */}
                    {isToken && (
                        <div className="mt-2">
                            <span className="text-xs text-accent-400">Token Transfer</span>
                        </div>
                    )}

                    {/* Flow Animation Dots */}
                    <div className="absolute flex gap-2 mt-4">
                        {[...Array(3)].map((_, i) => (
                            <div
                                key={i}
                                className="w-2 h-2 rounded-full bg-primary-500 animate-pulse"
                                style={{ animationDelay: `${i * 0.3}s` }}
                            />
                        ))}
                    </div>
                </div>

                {/* To Address */}
                <div className="flex-1 max-w-[140px]">
                    <div className="glass-light rounded-xl p-4 text-center relative overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-br from-pink-500/10 to-transparent" />
                        <div className="relative">
                            <div className="w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center">
                                <span className="text-xl">{isContract ? '📄' : '👤'}</span>
                            </div>
                            <p className="text-xs text-gray-500 mb-1">
                                {isContract ? 'Contract' : 'Receiver'}
                            </p>
                            <p className="text-xs font-mono text-gray-300 truncate" title={to}>
                                {toName || formatAddress(to)}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Transaction Type */}
            <div className="mt-6 text-center flex justify-center gap-2 flex-wrap">
                <span className={`badge ${isToken ? 'badge-accent' : isContract ? 'badge-info' : 'badge-success'}`}>
                    {isToken ? `${tokenSymbol} Transfer` : isContract ? 'Contract Interaction' : 'ETH Transfer'}
                </span>
                {toName && (
                    <span className="badge badge-warning">{toName}</span>
                )}
            </div>

            {/* Additional Info */}
            <div className="mt-4 grid grid-cols-2 gap-4 text-center">
                <div className="glass-light rounded-lg p-3">
                    <p className="text-xs text-gray-500">{isToken ? 'Token' : 'USD Value (approx)'}</p>
                    <p className="text-lg font-semibold text-white">
                        {isToken ? tokenSymbol : `$${usdValue?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
                    </p>
                </div>
                <div className="glass-light rounded-lg p-3">
                    <p className="text-xs text-gray-500">Transfer Size</p>
                    <p className="text-lg font-semibold text-white">
                        {isToken
                            ? (tokenAmount > 10000 ? 'Large' : tokenAmount > 100 ? 'Medium' : 'Small')
                            : (value > 10 ? 'High Value' : value > 1 ? 'Medium' : 'Small')
                        }
                    </p>
                </div>
            </div>
        </div>
    )
}
