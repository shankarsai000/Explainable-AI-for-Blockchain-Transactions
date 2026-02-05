export default function FraudRiskMeter({ riskScore, riskLevel, riskFactors }) {
    const getColor = () => {
        if (riskLevel === 'LOW') return { main: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' }
        if (riskLevel === 'MEDIUM') return { main: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)' }
        if (riskLevel === 'HIGH') return { main: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)' }
        if (riskLevel === 'CRITICAL') return { main: '#dc2626', bg: 'rgba(220, 38, 38, 0.1)' }
        return { main: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)' }
    }

    const colors = getColor()
    const percentage = Math.min(riskScore * 100, 100)
    const rotation = (percentage / 100) * 180 - 90

    return (
        <div className="glass rounded-2xl p-6 card-hover">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span>🛡️</span> Fraud Risk Analysis
            </h3>

            {/* Gauge */}
            <div className="flex justify-center mb-6">
                <div className="relative w-48 h-24 overflow-hidden">
                    {/* Background arc */}
                    <div
                        className="absolute inset-0 rounded-t-full"
                        style={{
                            background: `conic-gradient(from 180deg, 
                #10b981 0deg 60deg, 
                #f59e0b 60deg 120deg, 
                #ef4444 120deg 180deg,
                transparent 180deg 360deg)`,
                            opacity: 0.2,
                        }}
                    />

                    {/* Colored arc */}
                    <div
                        className="absolute inset-0 rounded-t-full"
                        style={{
                            background: `conic-gradient(from 180deg, 
                ${colors.main} 0deg ${percentage * 1.8}deg, 
                transparent ${percentage * 1.8}deg 180deg,
                transparent 180deg 360deg)`,
                        }}
                    />

                    {/* Center mask */}
                    <div className="absolute inset-4 bg-dark-800 rounded-t-full" />

                    {/* Needle */}
                    <div
                        className="absolute bottom-0 left-1/2 w-1 h-16 origin-bottom transition-transform duration-1000"
                        style={{
                            background: `linear-gradient(to top, ${colors.main}, ${colors.main}88)`,
                            transform: `translateX(-50%) rotate(${rotation}deg)`,
                            boxShadow: `0 0 10px ${colors.main}`,
                        }}
                    />

                    {/* Center dot */}
                    <div
                        className="absolute bottom-0 left-1/2 w-4 h-4 rounded-full transform -translate-x-1/2 translate-y-1/2"
                        style={{ background: colors.main }}
                    />
                </div>
            </div>

            {/* Score and Level */}
            <div className="text-center mb-6">
                <p
                    className="text-4xl font-bold mb-1"
                    style={{ color: colors.main }}
                >
                    {(riskScore * 100).toFixed(1)}%
                </p>
                <p
                    className="text-lg font-semibold uppercase tracking-wide"
                    style={{ color: colors.main }}
                >
                    {riskLevel} Risk
                </p>
            </div>

            {/* Risk Factors */}
            {riskFactors && riskFactors.length > 0 && (
                <div>
                    <p className="text-sm text-gray-400 mb-2">Risk Factors</p>
                    <ul className="space-y-2">
                        {riskFactors.map((factor, idx) => (
                            <li
                                key={idx}
                                className="flex items-start gap-2 text-sm text-gray-300 bg-dark-700/50 rounded-lg px-3 py-2"
                            >
                                <span className="text-xs mt-0.5">•</span>
                                <span>{factor}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}
