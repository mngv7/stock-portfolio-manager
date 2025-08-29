const API_URL = import.meta.env.VITE_API_URL;

export interface Trade {
    ticker: string
    avg_price: number
    quantity: number
    fee: number
    timestamp: number
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

export async function getPortfolioValue(jwt: string) {
  const response = await fetch(`${API_URL}/portfolio/value`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${jwt}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Error fetching portfolio value: ${response.status}`);
  }

  return response.json();
}

export async function getMonteCarloForecast(jwt: string) {
    const response = await fetch(`${API_URL}/portfolio/forecast`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`,
        }
    });

    if (!response.ok) {
        throw new Error(`Error calculating monte carlo forecast ${response.status}`);
    }

    return response.json();
}