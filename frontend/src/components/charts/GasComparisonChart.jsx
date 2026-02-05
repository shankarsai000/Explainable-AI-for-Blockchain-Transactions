import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

export default function GasComparisonChart({ predicted, actual, efficiency, feeUsd, explanation }) {
    const data = [
        { name: 'Predicted', value: predicted, fill: '#6366f1' },
        { name: 'Actual', value: actual, fill: '#8b5cf6' },
    ]

    const difference = actual - predicted
    const diffPercent = predicted > 0 ? ((difference / predicted) * 100).toFixed(1) : 0

    const getEfficiencyColor = () => {
        if (efficiency === 'EXCELLENT') return '#10b981'
        if (efficiency === 'NORMAL') return '#6366f1'
        if (efficiency === 'ABOVE_AVERAGE') return '#f59e0b'
        if (efficiency === 'CONGESTED' || efficiency === 'HIGH') return '#ef4444'
        return '#6b7280'
    }

    const getEfficiencyText = () => {
        if (efficiency === 'EXCELLENT') return 'Below predicted - Great timing!'
        if (efficiency === 'NORMAL') return 'Within expected range'
        if (efficiency === 'ABOVE_AVERAGE') return 'Higher than average'
        if (efficiency === 'CONGESTED') return 'Network congestion detected'
        if (efficiency === 'HIGH') return 'Significantly elevated'
        return 'Unknown'
    }

    // Use provided explanation or generate default
    const gasExplanation = explanation || getEfficiencyText()

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="glass rounded-lg px-3 py-2 border border-white/10">
                    <p className="text-white font-medium">{payload[0].payload.name}</p>
                    <p className="text-gray-300">{payload[0].value.toFixed(2)} gwei</p>
                </div>
            )
        }
        return null
    }

    return (
        <div className="glass rounded-2xl p-6 card-hover">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <span>⛽</span> Gas Fee Analysis
            </h3>

            {/* Chart */}
            <div className="h-48 mb-4">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" barSize={24}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#2a2a38" horizontal={false} />
                        <XAxis type="number" stroke="#9ca3af" fontSize={12} tickFormatter={(v) => `${v.toFixed(0)}`} />
                        <YAxis type="category" dataKey="name" stroke="#9ca3af" fontSize={12} width={70} />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                    <p className="text-xs text-gray-500 uppercase">Predicted</p>
                    <p className="text-xl font-bold text-primary-400">{predicted.toFixed(1)}</p>
                    <p className="text-xs text-gray-500">gwei</p>
                </div>
                <div className="text-center">
                    <p className="text-xs text-gray-500 uppercase">Actual</p>
                    <p className="text-xl font-bold text-accent-400">{actual.toFixed(1)}</p>
                    <p className="text-xs text-gray-500">gwei</p>
                </div>
                <div className="text-center">
                    <p className="text-xs text-gray-500 uppercase">Difference</p>
                    <p
                        className="text-xl font-bold"
                        style={{ color: difference > 0 ? '#ef4444' : '#10b981' }}
                    >
                        {difference > 0 ? '+' : ''}{diffPercent}%
                    </p>
                    <p className="text-xs text-gray-500">vs predicted</p>
                </div>
            </div>

            {/* USD Fee Display */}
            {feeUsd > 0 && (
                <div className="text-center mb-4 py-2 glass-light rounded-lg">
                    <p className="text-sm text-gray-400">Transaction Fee</p>
                    <p className="text-2xl font-bold text-white">${feeUsd.toFixed(2)} USD</p>
                </div>
            )}

            {/* Efficiency Badge with Explanation */}
            <div
                className="rounded-xl px-4 py-3"
                style={{ backgroundColor: `${getEfficiencyColor()}15`, border: `1px solid ${getEfficiencyColor()}30` }}
            >
                <p className="font-semibold text-center" style={{ color: getEfficiencyColor() }}>
                    {efficiency}
                </p>
                <p className="text-sm text-gray-400 mt-1 text-center">{gasExplanation}</p>
            </div>
        </div>
    )
}
