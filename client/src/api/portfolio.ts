const API_URL = 'http://localhost:8080'

export interface Trade {
    ticker: string
    avg_price: number
    quantity: number
    fee: number
}

export async function getPortfolioAssets(jwt: string) {
    const response = await fetch(`${API_URL}/portfolio/assets`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`  
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json();
}

export async function postTrade(jwt: string, trade: Trade) {
    const response = await fetch(`${API_URL}/portfolio/trades`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`  
        },
        body: JSON.stringify(trade)
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json()
}

export async function getTrades(jwt: string) {
    const response = await fetch(`${API_URL}/portfolio/trades`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`  
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json()
}