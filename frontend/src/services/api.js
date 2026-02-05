import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
    baseURL: API_BASE,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

export const explainTransaction = async (txHash) => {
    const response = await api.post('/explain', {
        tx_hash: txHash,
        include_visualizations: true,
        language: 'en',
    })
    return response.data
}

export const decodeTransaction = async (txHash) => {
    const response = await api.post('/decode_tx', { tx_hash: txHash })
    return response.data
}

export const predictFraud = async (walletFeatures) => {
    const response = await api.post('/predict/fraud', walletFeatures)
    return response.data
}

export const predictGas = async (txFeatures) => {
    const response = await api.post('/predict/gas', txFeatures)
    return response.data
}

export const classifyTransaction = async (txFeatures) => {
    const response = await api.post('/predict/tx_type', txFeatures)
    return response.data
}

export const checkHealth = async () => {
    const response = await api.get('/health')
    return response.data
}

export default api
