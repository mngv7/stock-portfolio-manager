import { useEffect, useState } from "react";
import { getPortfolioAssets } from "../api/portfolio";
import PortfolioChart from "./PortfolioChart";

function Portfolio() {
    const token = localStorage.getItem("jwt");
    const [assets, setAssets] = useState<{ [ticker: string]: number} | null>(null);

    useEffect(() => {
        const getAssets = async () => {
            if (token) {
                const response = await getPortfolioAssets(token);
                setAssets(response);
            }
        };

        getAssets();
    }, [token]);

    if (!assets) {
        return (
            <div>
                Loading...
            </div>
        )
    }

    return (
        <div>
            {Object.entries(assets).map(([ticker, quantity]) => (
                <div key={ticker}>
                    {ticker} - {quantity}
                </div>
            ))}
            <PortfolioChart />
        </div>
    )
}

export default Portfolio;