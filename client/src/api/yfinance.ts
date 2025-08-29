const API_URL = import.meta.env.VITE_API_URL;

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