// TypeScript file
// @ts-ignore
import fetchParameterLocal from '../utils/parameterStore'

const API_URL = await fetchParameterLocal(`/n11592931/prod/${import.meta.env.VITE_BUILD_ENV}/api_url`);

export async function fetchCurrentPrice(ticker: string) {
    const response = await fetch(`${API_URL}/price?ticker=${encodeURIComponent(ticker)}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json()
}