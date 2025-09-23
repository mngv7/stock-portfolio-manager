import { useState } from "react";
import { getMonteCarloForecast } from "../../api/portfolio";
import './Analysis.css'
import { decodeJwt } from "../../api/auth";

function Analysis() {
    const token = localStorage.getItem("jwt");
    const [expectedReturn, setExpectedReturn] = useState(0);
    const [volatility, setVolatility] = useState(0);
    const [fifthPercentile, setFifthPercentile] = useState(0);
    const [ninetyFifthPercentile, setNinetyFifthPercentile] = useState(0);
    const [var95, setVar95] = useState(0);
    const [_, setDistribution] = useState<number[]>([]);
    const [loading, setLoading] = useState(false);
    const [isPremiumUser, setIsPremiumUser] = useState(false);

    const executeMonteCarlo = async () => {
        if (token && isPremiumUser) {
            setLoading(true);
            const response = await getMonteCarloForecast(token);
            setLoading(false);
            setExpectedReturn(response["expected_return"]);
            setVolatility(response["volatility"]);
            setFifthPercentile(response["5th_percentile"]);
            setNinetyFifthPercentile(response["95th_percentile"]);
            setVar95(response["VaR_95"]);
            setDistribution(response["distribution"]);
        }
    };

    const verifyPremiumUser = async () => {
        if (!token) return;
        const response = await decodeJwt(token);
        if (response["cognito:groups"].includes("premium-user")) {
            setIsPremiumUser(true);
        } else {
            setIsPremiumUser(false);
        }
    }

    verifyPremiumUser();

    return (
        <div className="analysis">
            <h1>Analysis</h1>
            {loading && <p>Running Simulation...</p>}
            Expected Return: {expectedReturn}
            <br />
            Volatility: {volatility}
            <br />
            5th Percentile: {fifthPercentile}
            <br />
            95th Percentile: {ninetyFifthPercentile}
            <br />
            Value at Risk 95: {var95}
            <button onClick={executeMonteCarlo}>
            {isPremiumUser ? "Run Simulation": "Upgrade to Premium"}
            </button>
        </div>
    );
}

export default Analysis;