import { useEffect, useState } from "react";
import { getPortfolioAssets } from "../api/portfolio";
import PortfolioChart from "./PortfolioChart";
import { PieChart } from '@mui/x-charts/PieChart';
import '../assets/Portfolio.css'

function Portfolio({ trigger }: { trigger: number}) {
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
    }, [token, trigger]);

    if (!assets) {
        return (
            <div>
                Loading...
            </div>
        )
    }

    const greenShades = [
        '#1b3a1b',
        '#2c5f2d',
        '#3cb371',
        '#66cdaa',
        '#98fb98',
        '#c8facc'
    ];


    const dataWithColors = Object.entries(assets).map(([ticker, quantity], index) => ({
        label: ticker,
        value: quantity,
        color: greenShades[index]
    }));

    const settings = {
        width: 250,
        height: 250,
    };

    return (
        <div className="portfolio">
            <h1>Portfolio</h1>
            <div className="charts">
                <div className="line-chart">
                    <PortfolioChart />
                </div>
                <div className="pie-chart">
                <PieChart
                    series={[{ innerRadius: 50, outerRadius: 100, data: dataWithColors, arcLabel: 'value'}] }
                    {...settings}
                />

                </div>
            </div>
        </div>
    )
}

export default Portfolio;