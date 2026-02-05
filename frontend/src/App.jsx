import { useState } from 'react'
import { Toaster, toast } from 'react-hot-toast'
import Header from './components/Header'
import TransactionInput from './components/TransactionInput'
import ExplanationPanel from './components/ExplanationPanel'
import FraudRiskMeter from './components/charts/FraudRiskMeter'
import GasComparisonChart from './components/charts/GasComparisonChart'
import TransactionClassification from './components/TransactionClassification'
import TokenFlowDiagram from './components/charts/TokenFlowDiagram'
import LoadingState from './components/LoadingState'
import ParticleBackground from './components/ParticleBackground'
import { explainTransaction } from './services/api'

function App() {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleSubmit = async (txHash) => {
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const data = await explainTransaction(txHash)
            setResult(data)
            toast.success('Transaction analyzed successfully!')
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message || 'Failed to analyze transaction'
            setError(errorMessage)
            toast.error(errorMessage)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen relative">
            <ParticleBackground />
            <Toaster
                position="top-right"
                toastOptions={{
                    style: {
                        background: '#1a1a24',
                        color: '#f3f4f6',
                        border: '1px solid rgba(255,255,255,0.1)',
                    },
                }}
            />

            <div className="relative z-10">
                <Header />

                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {/* Hero Section */}
                    <section className="text-center mb-12">
                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">
                            <span className="gradient-text">Blockchain Transaction</span>
                            <br />
                            <span className="text-white">Explainer</span>
                        </h1>
                        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto mb-8">
                            AI-powered analysis that transforms complex blockchain transactions
                            into clear, actionable insights.
                        </p>
                    </section>

                    {/* Input Section */}
                    <section className="mb-12">
                        <TransactionInput onSubmit={handleSubmit} loading={loading} />
                    </section>

                    {/* Loading State */}
                    {loading && <LoadingState />}

                    {/* Error State */}
                    {error && (
                        <div className="glass rounded-2xl p-6 border-red-500/30 text-center mb-8">
                            <div className="text-red-400 text-lg mb-2">⚠️ Error</div>
                            <p className="text-gray-300">{error}</p>
                        </div>
                    )}

                    {/* Results */}
                    {result && !loading && (
                        <div className="space-y-8 animate-fade-in">
                            {/* Main Explanation */}
                            <ExplanationPanel
                                explanation={result.natural_explanation}
                                summary={result.summary}
                                sections={result.sections}
                                transaction={result.transaction}
                                contextInsight={result.context_insight}
                                classification={result.classification}
                            />

                            {/* Analytics Grid */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {/* Fraud Risk */}
                                <FraudRiskMeter
                                    riskScore={result.fraud_analysis?.risk_score || 0}
                                    riskLevel={result.fraud_analysis?.risk_level || 'UNKNOWN'}
                                    riskFactors={result.fraud_analysis?.risk_factors || []}
                                />

                                {/* Gas Analysis */}
                                <GasComparisonChart
                                    predicted={result.gas_analysis?.predicted_gas_gwei || 0}
                                    actual={result.gas_analysis?.actual_gas_gwei || 0}
                                    efficiency={result.gas_analysis?.efficiency || 'NORMAL'}
                                    feeUsd={result.gas_analysis?.fee_usd || 0}
                                    explanation={result.gas_analysis?.explanation}
                                />
                            </div>

                            {/* Classification & Flow */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                <TransactionClassification
                                    category={result.classification?.category || 'Unknown'}
                                    confidence={result.classification?.confidence || 0}
                                    allCategories={result.classification?.all_categories || {}}
                                />

                                <TokenFlowDiagram
                                    from={result.transaction?.from_address || ''}
                                    to={result.transaction?.to_address || ''}
                                    value={result.transaction?.value_eth || 0}
                                    isContract={result.transaction?.contract_interaction || false}
                                    isToken={result.transaction?.is_token_transfer || false}
                                    tokenSymbol={result.transaction?.token_info?.symbol}
                                    tokenAmount={result.transaction?.token_amount}
                                    toName={result.transaction?.to_address_info?.name}
                                />
                            </div>

                            {/* Recommendations */}
                            {result.recommendations && result.recommendations.length > 0 && (
                                <div className="glass rounded-2xl p-6 card-hover">
                                    <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                                        <span>💡</span> Recommendations
                                    </h3>
                                    <ul className="space-y-3">
                                        {result.recommendations.map((rec, idx) => (
                                            <li key={idx} className="flex items-start gap-3 text-gray-300">
                                                <span className="text-primary-400 mt-1">→</span>
                                                <span>{rec}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Empty State */}
                    {!result && !loading && !error && (
                        <div className="text-center py-16">
                            <div className="text-6xl mb-4 float">🔍</div>
                            <h3 className="text-xl font-semibold text-gray-300 mb-2">
                                Enter a Transaction Hash
                            </h3>
                            <p className="text-gray-500 max-w-md mx-auto">
                                Paste any Ethereum transaction hash above to get a complete AI-powered
                                analysis including fraud detection, gas insights, and more.
                            </p>
                        </div>
                    )}
                </main>

                {/* Footer */}
                <footer className="text-center py-8 text-gray-500 text-sm">
                    <p>Powered by AI & Machine Learning</p>
                    <p className="mt-1">© 2024 Blockchain Transaction Explainer</p>
                </footer>
            </div>
        </div>
    )
}

export default App
