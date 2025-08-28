import { useEffect, useState } from "react";
import { getMonteCarloForecast } from "../api/portfolio";
import '../assets/Analysis.css'

function Analysis() {
    const token = localStorage.getItem("jwt");
    const [triggerSimulation, setTriggerSimulation] = useState(0);
    const [expectedReturn, setExpectedReturn] = useState(0);
    const [volatility, setVolatility] = useState(0);
    const [fifthPercentile, setFifthPercentile] = useState(0);
    const [ninetyFifthPercentile, setNinetyFifthPercentile] = useState(0);
    const [var95, setVar95] = useState(0);
    const [distribution, setDistribution] = useState<number[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (triggerSimulation > 0) {
            const executeMonteCarlo = async () => {
                if (token) {
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

            executeMonteCarlo();
        }
    }, [triggerSimulation]);


    const handleSimulationExecute = () => {
        setTriggerSimulation(triggerSimulation + 1);
    }

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
            <button 
                value={triggerSimulation}
                onClick={handleSimulationExecute}
            >Run Simulation</button>
        </div>
    )
}

export default Analysis;