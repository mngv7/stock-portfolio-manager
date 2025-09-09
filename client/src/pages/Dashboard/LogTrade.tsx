import { useState } from "react";
import { postTrade } from "../../api/portfolio";
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs, { Dayjs } from 'dayjs';
import './LogTrade.css'

function LogTrade({ handleLogTrade }: { handleLogTrade: () => void}) {
    const token = localStorage.getItem("jwt");
    const [ticker, setTicker] = useState("");
    const [price, setPrice] = useState("");
    const [quantity, setQuantity] = useState("");
    const [fee, setFee] = useState("");
    const [date, setDate] = useState<Dayjs | null>(null);

    const logTrade = async() => {
        if (ticker && price && quantity && fee && date) {
            const epochDate = Math.floor(date.valueOf() / 1000);

            const trade = {
                ticker: ticker,
                avg_price: parseFloat(price),
                quantity: parseFloat(quantity),
                fee: parseFloat(fee),
                timestamp: epochDate
            };

            if (token) {
                await postTrade(token, trade);
            }
            setTicker("");
            setPrice("");
            setQuantity("");
            setFee("");
            setDate(null);
            handleLogTrade();
        }
    };

    return (
        <div className="log-trade-container">
            <h1>Trade</h1>
            <input 
                placeholder="Ticker" 
                maxLength={10}
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
            <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DemoContainer components={['DateTimePicker']}>
                <DateTimePicker
                    label="Trade Time"
                    value={date}
                    onChange={(e) => setDate(e)}
                    minTime={dayjs().hour(9).minute(30)}
                    maxTime={dayjs().hour(16).minute(0)}
                    shouldDisableDate={(day) => {
                        const dayOfWeek = day.day();
                        return dayOfWeek === 0 || dayOfWeek === 6
                    }}
                />
            </DemoContainer>
            </LocalizationProvider>
            <button onClick={logTrade}>Log Trade</button>
        </div>
    );
}

export default LogTrade;
