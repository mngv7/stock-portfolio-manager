import { useEffect, useState } from "react";
import { getReceiptS3Url, getTrades } from "../../api/portfolio";
import './TradesLog.css'
import { useNavigate } from "react-router-dom";

function TradesLog() {
    const navigate = useNavigate();
    const token = localStorage.getItem("jwt");

    // Trade searching
    const [loadTrades, setLoadTrades] = useState(0);
    const [tickerSort, setTickerSort] = useState('');
    const [tradeSearchResult, setTradeSearchResult] = useState([]);
    const [sortOrder, setSortOrder] = useState('asc');
    const [pageNumber, setPageNumber] = useState(1);
    const [totalTrades, setTotalTrades] = useState(0);

    // Generate S3 URL
    const [searchTimestamp, setSearchTimestamp] = useState<number | null>(null);
    const [searchTicker, setSearchTicker] = useState<string | null>(null);
    const [presignedUrl, setPresignedUrl] = useState("");

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

    const handleGeneratePresignedUrl = async () => {
        if (!token) return;

        if (searchTimestamp && searchTicker) {
            const response = await getReceiptS3Url(searchTimestamp, searchTicker, token);
            if (response.presigned_url) {
                setPresignedUrl(response.presigned_url);
                navigate(presignedUrl);
                setSearchTicker(null);
                setSearchTimestamp(null);
            }

        } else {
            console.log("Please enter a timestamp and ticker.");
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
    const maxPage = Math.max(1, Math.ceil(totalTrades / pageSize));

    return (
        <div className="trades-log-container">
            <h1>Trades</h1>
            <p>Search through trades</p>
            <div className="trades-log-header">
                <div>
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
                </div>

                <div>
                    <input 
                        placeholder="Timestamp"
                        value={searchTimestamp ?? ""}
                        onChange={(e) => setSearchTimestamp(Number(e.target.value))}
                    />
                    <input 
                        placeholder="Ticker"
                        value={searchTicker ?? ""}
                        onChange={(e) => setSearchTicker(e.target.value)}
                    />
                    <button onClick={handleGeneratePresignedUrl}>Generate</button>
                </div>
            </div>
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
