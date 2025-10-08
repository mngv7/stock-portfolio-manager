export interface Trade {
    ticker: string
    avg_price: number
    quantity: number
    fee: number
    timestamp: number
}

export async function getPortfolioAssets(jwt: string) {
    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/portfolio/assets`, {
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
    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/portfolio/trades`, {
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

export async function getTrades(jwt: string, pageNo: number = 1, pageSize: number = 10, ticker?: string, sortOrder?: string) {
    const params = new URLSearchParams()
    params.append("page_no", pageNo.toString());
    params.append("page_size", pageSize.toString());

    if (ticker) {
        params.append("ticker", ticker);
    }

    if (sortOrder) {
        params.append("sort_order", sortOrder);
    }

    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/portfolio/trades?${params.toString()}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${jwt}`
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json()
}

export async function getPortfolioHistoricalValue(jwt: string) {
    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/portfolio/value`, {
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
    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/portfolio/forecast`, {
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

export async function uploadReceipt(receipt_file: File, trade: Trade, jwt: string) {
    const formData = new FormData();

    formData.append("receipt_file", receipt_file);
    formData.append("trade", JSON.stringify(trade));

    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/receipt`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${jwt}`,
        },
        body: formData
    });

    if (!response.ok) {
        throw new Error("Failed to upload file.");
    }

    return "File uploaded!"
}

export async function getReceiptS3Url(timestamp: number, ticker: string, jwt: string) {
    const params = new URLSearchParams();
    params.append("timestamp", timestamp.toString());
    params.append("ticker", ticker);

    const response = await fetch(`https://portfoliomanagerapi.cab432.com/v1/api/v1/receipt?${params}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${jwt}`,
        }
    });

    if (!response.ok) {
        throw new Error("Failed to get trade receipt.");
    }

    return response.json();
}

export async function fetchPortfolioResult(jwt: string) {
    const response = await fetch(`endpoint`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${jwt}`
        }
    });

    if (!response.ok) {
        throw new Error("Could not fetch portfolio result");
    }

    return response.json();
}