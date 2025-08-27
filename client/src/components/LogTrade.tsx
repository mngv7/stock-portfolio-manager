import { useState } from "react";
import { postTrade } from "../api/portfolio";

function LogTrade() {
    const token = localStorage.getItem("jwt");
    const [ticker, setTicker] = useState('');
    const [price, setPrice] = useState('');
    const [quantity, setQuantity] = useState('');
    const [fee, setFee] = useState('');

    const handleLogTrade = async() => {
        const trade = {
            ticker,
            avg_price: parseFloat(price),
            quantity: parseFloat(quantity),
            fee: parseFloat(fee)
        };

        if (token) {
            await postTrade(token, trade);
        }

        setTicker('');
        setPrice('');
        setQuantity('');
        setFee('');
    };

    return (
        <div className="log-trade-container">
            <input 
                placeholder="Ticker" 
                value={ticker} 
                onChange={(e) => setTicker(e.target.value)} 
            />
            <br/>
            <input 
                placeholder="Price" 
                type="number" 
                value={price} 
                onChange={(e) => setPrice(e.target.value)} 
            />
            <br/>
            <input 
                placeholder="Quantity" 
                type="number" 
                value={quantity} 
                onChange={(e) => setQuantity(e.target.value)} 
            />
            <br/>
            <input 
                placeholder="Fee" 
                type="number" 
                value={fee} 
                onChange={(e) => setFee(e.target.value)} 
            />
            <br/>
            <button onClick={handleLogTrade}>Log Trade</button>
        </div>
    );
}

export default LogTrade;
