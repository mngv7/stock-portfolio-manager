import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect, useState } from 'react';
import { getPortfolioHistoricalValue } from '../api/portfolio';

function PortfolioChart() {
    const token = localStorage.getItem("jwt");
    const [portfolioHistory, setPortfolioHistory] = useState<{ [date: string]: number } | null>(null);

    useEffect(() => {
        const fetchPortfolioHistory = async () => {
            if (token) {
                try {
                    const history = await getPortfolioHistoricalValue(token);
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

    if (!lineChartData) {
        return (
            <p>Loading...</p>
        )
    }

    return (
        <div>
            <LineChart
                xAxis={[{ scaleType: 'time', data: lineChartData.map((d) => d.x) }]}
                series={[
                    {
                        data: formattedData,
                        showMark: false,
                        color: '#3f5a36',
                        curve: 'linear'
                    },
                ]}
                height={300}
            />
        </div>
    );
}

export default PortfolioChart;
