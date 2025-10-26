import { useState } from "react";
import { fetchMonteCarloResult, postMonteCarloForecastTask } from "../../api/portfolio";
import './Analysis.css'
import { decodeJwt } from "../../api/auth";

type Result = {
    expected_return: number;
    volatility: number;
    '5th_percentile': number;
    '95th_percentile': number;
    VaR_95: number;
    distribution: number[];
};

function pollResult(jwt: string, onResult: (result: Result) => void) {
    const poll = async () => {
        const result = await fetchMonteCarloResult(jwt);
        if (result) {
            onResult(result);
        } else {
            setTimeout(poll, 5000);
        }
    };
    poll();
}

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

    const setSimulationResults = (result: Result) => {
        setLoading(false);
        setExpectedReturn(result.expected_return);
        setVolatility(result.volatility);
        setFifthPercentile(result["5th_percentile"]);
        setNinetyFifthPercentile(result["95th_percentile"]);
        setVar95(result.VaR_95);
        setDistribution(result.distribution);
    }

    const executeMonteCarlo = async () => {
        if (token && isPremiumUser) {
            setLoading(true);
            await postMonteCarloForecastTask(token);
            pollResult(token, (result) => setSimulationResults(result))
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
                {isPremiumUser ? "Run Simulation" : "Upgrade to Premium"}
            </button>
        </div>
    );
}

export default Analysis;