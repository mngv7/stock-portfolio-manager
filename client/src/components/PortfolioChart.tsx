import { LineChart } from '@mui/x-charts/LineChart'
import { useEffect, useState } from 'react';
import { getTrades } from '../api/portfolio';
import { getTickerDailyHistory } from '../api/yfinance';

type Trade = {
  ticker: string;
  avg_price: number;
  quantity: number;
  fee: number;
  timestamp: number;
};

function PortfolioChart() {
    const token = localStorage.getItem("jwt");
    const [trades, setTrades] = useState<[Trade] | null>(null);
    const [tradeHistory, setTradeHistory] = useState(null);

    useEffect(() => {
        const tickerParams = {
            ticker: 'AAPL',
            timestamp: 1724720034
        }
        const fetchTickerHistory = async() => {
            const history = await getTickerDailyHistory(tickerParams);
            setTradeHistory(history)
        }

        const fetchTrades = async() => {
            if (token) {
                const trades = await getTrades(token);
                setTrades(trades);
            }
        }

        fetchTrades();
        fetchTickerHistory();
    }, []);


    console.log(trades);
    console.log(tradeHistory);
    return (
        <div>
            <LineChart
                xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
                series={[
                    {
                    data: [4, 5.5, 2, 8.5, 1.5, 5],
                    },
                ]}
                height={300}
            />
        </div>
    )
}

export default PortfolioChart;