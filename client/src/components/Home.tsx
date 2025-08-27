import { Routes, Route } from 'react-router-dom';
import LogTrade from "./LogTrade";
import NavBar from "./NavBar";
import Portfolio from "./Portfolio";
import Analysis from './Analysis';

function Home() {
    return (
        <>
            <NavBar />
            <div className="content">
                <Routes>
                    <Route path="portfolio" element={<Portfolio />} />
                    <Route path="trade" element={<LogTrade />} />
                    <Route path="analysis" element={<Analysis />} />
                </Routes>
            </div>
        </>
    )
}

export default Home;