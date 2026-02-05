import { useState } from 'react'

export default function TransactionInput({ onSubmit, loading }) {
    const [txHash, setTxHash] = useState('')
    const [error, setError] = useState('')

    const validateHash = (hash) => {
        const pattern = /^0x[a-fA-F0-9]{64}$/
        return pattern.test(hash)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        setError('')

        const trimmedHash = txHash.trim()

        if (!trimmedHash) {
            setError('Please enter a transaction hash')
            return
        }

        if (!validateHash(trimmedHash)) {
            setError('Invalid transaction hash format. Must be 0x followed by 64 hex characters.')
            return
        }

        onSubmit(trimmedHash)
    }

    const handlePaste = async () => {
        try {
            const text = await navigator.clipboard.readText()
            if (text) {
                setTxHash(text.trim())
                setError('')
            }
        } catch (err) {
            console.error('Failed to paste:', err)
        }
    }

    // Example transaction for demo
    const setExample = () => {
        setTxHash('0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060')
        setError('')
    }

    return (
        <div className="glass rounded-2xl p-6 md:p-8 glow-primary card-hover">
            <form onSubmit={handleSubmit}>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                    Transaction Hash
                </label>

                <div className="relative">
                    <input
                        type="text"
                        value={txHash}
                        onChange={(e) => {
                            setTxHash(e.target.value)
                            setError('')
                        }}
                        placeholder="0x..."
                        className="w-full px-4 py-4 bg-dark-700 border border-white/10 rounded-xl 
                       text-white font-mono text-sm placeholder-gray-500
                       focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500
                       transition-all duration-200"
                        disabled={loading}
                    />

                    <button
                        type="button"
                        onClick={handlePaste}
                        className="absolute right-3 top-1/2 -translate-y-1/2 px-3 py-1.5 
                       text-xs text-gray-400 hover:text-white bg-dark-600 
                       rounded-lg hover:bg-dark-500 transition-colors"
                    >
                        Paste
                    </button>
                </div>

                {error && (
                    <p className="mt-2 text-sm text-red-400">{error}</p>
                )}

                <div className="mt-4 flex flex-col sm:flex-row gap-3">
                    <button
                        type="submit"
                        disabled={loading}
                        className="flex-1 btn-gradient px-6 py-3 rounded-xl font-semibold text-white
                       disabled:opacity-50 disabled:cursor-not-allowed
                       flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                <span>Analyzing...</span>
                            </>
                        ) : (
                            <>
                                <span>🔍</span>
                                <span>Analyze Transaction</span>
                            </>
                        )}
                    </button>

                    <button
                        type="button"
                        onClick={setExample}
                        disabled={loading}
                        className="px-6 py-3 rounded-xl font-medium text-gray-400 
                       bg-dark-600 hover:bg-dark-500 hover:text-white
                       disabled:opacity-50 transition-colors"
                    >
                        Use Example
                    </button>
                </div>
            </form>

            <p className="mt-4 text-xs text-gray-500 text-center">
                Supports Ethereum mainnet transactions • Real-time analysis
            </p>
        </div>
    )
}
