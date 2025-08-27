import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect, useState } from 'react';
import { getPortfolioValue } from '../api/portfolio';

function PortfolioChart() {
    const token = localStorage.getItem("jwt");
    const [portfolioHistory, setPortfolioHistory] = useState<{ [date: string]: number } | null>(null);

    useEffect(() => {
        const fetchPortfolioHistory = async () => {
            if (token) {
                try {
                    const history = await getPortfolioValue(token);
                    setPortfolioHistory(history);
                } catch (err) {
                    console.error(err);
                }
            }
        };

        fetchPortfolioHistory();
    }, [token]);

    const lineChartData = portfolioHistory
        ? Object.entries(portfolioHistory).map(([date, value]) => ({
              x: new Date(date),
              y: value,
          }))
        : [];

    const formattedData = lineChartData.map((d) => d.y)

    return (
        <div>
            <LineChart
                xAxis={[{ scaleType: 'time', data: lineChartData.map((d) => d.x) }]}
                series={[
                    {
                        data: formattedData, showMark: false
                    },
                ]}
                height={300}
            />
        </div>
    );
}

export default PortfolioChart;
