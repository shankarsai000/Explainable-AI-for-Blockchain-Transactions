export default function TransactionClassification({ category, confidence, allCategories }) {
    const getCategoryIcon = (cat) => {
        const icons = {
            'Simple Transfer': '💸',
            'Token Transfer': '🪙',
            'DEX Swap': '🔄',
            'NFT Transaction': '🖼️',
            'Staking/Yield': '📈',
            'Bridge Transfer': '🌉',
            'Contract Deployment': '📄',
            'Governance Vote': '🗳️',
            'Lending/Borrowing': '🏦',
            'Other': '❓',
        }
        return icons[cat] || '📋'
    }

    const getCategoryColor = (cat) => {
        const colors = {
            'Simple Transfer': 'from-blue-500 to-cyan-500',
            'Token Transfer': 'from-yellow-500 to-orange-500',
            'DEX Swap': 'from-purple-500 to-pink-500',
            'NFT Transaction': 'from-pink-500 to-rose-500',
            'Staking/Yield': 'from-green-500 to-emerald-500',
            'Bridge Transfer': 'from-indigo-500 to-blue-500',
            'Contract Deployment': 'from-gray-500 to-slate-500',
            'Governance Vote': 'from-amber-500 to-yellow-500',
            'Lending/Borrowing': 'from-teal-500 to-cyan-500',
        }
        return colors[cat] || 'from-gray-500 to-gray-600'
    }

    // Sort categories by probability
    const sortedCategories = Object.entries(allCategories || {})
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)

    return (
        <div className="glass rounded-2xl p-6 card-hover">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span>🏷️</span> Transaction Classification
            </h3>

            {/* Primary Category */}
            <div className="mb-6">
                <div className={`inline-flex items-center gap-3 px-5 py-3 rounded-xl 
                         bg-gradient-to-r ${getCategoryColor(category)} 
                         shadow-lg`}>
                    <span className="text-2xl">{getCategoryIcon(category)}</span>
                    <div>
                        <p className="font-bold text-white text-lg">{category}</p>
                        <p className="text-white/80 text-sm">
                            {(confidence * 100).toFixed(1)}% confidence
                        </p>
                    </div>
                </div>
            </div>

            {/* Confidence Bar */}
            <div className="mb-6">
                <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Model Confidence</span>
                    <span className="text-white font-medium">{(confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="h-3 bg-dark-600 rounded-full overflow-hidden">
                    <div
                        className={`h-full bg-gradient-to-r ${getCategoryColor(category)} 
                        transition-all duration-1000 ease-out rounded-full`}
                        style={{ width: `${confidence * 100}%` }}
                    />
                </div>
            </div>

            {/* All Categories */}
            {sortedCategories.length > 1 && (
                <div>
                    <p className="text-sm text-gray-400 mb-3">All Predictions</p>
                    <div className="space-y-2">
                        {sortedCategories.map(([cat, prob]) => (
                            <div key={cat} className="flex items-center gap-3">
                                <span className="text-sm">{getCategoryIcon(cat)}</span>
                                <div className="flex-1">
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-gray-400">{cat}</span>
                                        <span className="text-gray-300">{(prob * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="h-1.5 bg-dark-600 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gray-500 rounded-full transition-all duration-500"
                                            style={{ width: `${prob * 100}%` }}
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
