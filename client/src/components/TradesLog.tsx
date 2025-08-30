import { useEffect, useState } from "react";
import { getTrades } from "../api/portfolio";
import '../assets/TradesLog.css'

function TradesLog() {
    const [loadTrades, setLoadTrades] = useState(0);
    const [tickerSort, setTickerSort] = useState('');
    const token = localStorage.getItem("jwt");
    const [tradeSearchResult, setTradeSearchResult] = useState([]);
    const [sortOrder, setSortOrder] = useState('asc');
    const [pageNumber, setPageNumber] = useState(1);
    const [totalTrades, setTotalTrades] = useState(0);
    const pageSize = 5;

    const handleLoad = () => {
        setLoadTrades((prev) => prev + 1);
    };

    const handlePageIncrease = () => {
        const maxPage = Math.ceil(totalTrades / pageSize);
        if (pageNumber < maxPage) {
            setPageNumber((prev) => prev + 1);
            handleLoad();
        }
    };

    const handlePageDecrease = () => {
        if (pageNumber > 1) {
            setPageNumber((prev) => prev - 1);
            handleLoad();
        }
    };

    useEffect(() => {
        const callGetTrades = async () => {
            if (token) {
                const response = await getTrades(token, pageNumber, pageSize, tickerSort, sortOrder);
                setTradeSearchResult(response.trade_list || []);
                setTotalTrades(response.length || 0);
            }
        };

        callGetTrades();
    }, [loadTrades, pageNumber, sortOrder, tickerSort, token]);
    console.log(totalTrades);
    const maxPage = Math.max(1, Math.ceil(totalTrades / pageSize));

    return (
        <div className="trades-log-container">
            <h1>Trades</h1>
            <p>Search through trades</p>
            <input
                placeholder="Ticker"
                maxLength={10}
                value={tickerSort}
                onChange={(e) => setTickerSort(e.target.value)}
            />
            <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
            </select>
            <button onClick={handleLoad}>Search</button>
            <button onClick={() => {setTradeSearchResult([]); setTotalTrades(0);}}>Clear</button>
            <br />
            
            <pre>{JSON.stringify(tradeSearchResult, null, 2)}</pre>
            
            <div className="search-footer">
                <p>Display {pageSize} items per page. Page {pageNumber} of {maxPage}.</p>

                <button onClick={handlePageDecrease} disabled={pageNumber === 1}>
                    &larr;
                </button>
                <button onClick={handlePageIncrease} disabled={pageNumber === maxPage}>
                    &rarr;
                </button>
            </div>
        </div>
    );
}

export default TradesLog;
