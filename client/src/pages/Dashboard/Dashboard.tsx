import Analysis from "./Analysis";
import LogTrade from "./LogTrade";
import Portfolio from "./Portfolio";
import './Dashboard.css'
import { useState } from "react";
import TradesLog from "./TradesLog";

function Dashboard() {
    const [reloadGraph, setReloadGraph] = useState(0);

    const handleNewTrade = () => {
        setReloadGraph(reloadGraph + 1)
    }

    return (
        <div>
            <div className="dashboard">
                <Portfolio trigger={reloadGraph}/>
                <div className="trade-analysis">
                    <LogTrade handleLogTrade={handleNewTrade}/>
                    <Analysis />
                </div>
                <TradesLog />
            </div>
        </div>
    )   
}

export default Dashboard;