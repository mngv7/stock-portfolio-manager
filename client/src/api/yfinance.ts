const API_URL = 'http://localhost:8080'

export interface TickerParams {
    ticker: string,
    timestamp: number
}

export async function getTickerDailyHistory({ ticker, timestamp }: TickerParams) {
    const params = new URLSearchParams({
        ticker,
        timestamp: timestamp.toString()
    });

    const response = await fetch(`${API_URL}/ticker/price?${params.toString()}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json();
}
