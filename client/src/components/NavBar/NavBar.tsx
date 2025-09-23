import { NavLink } from "react-router-dom";
import './NavBar.css'
import { decodeJwt, upgradeToPremiumUser } from "../../api/auth";
import { useState } from "react";

function NavBar() {
    const token = localStorage.getItem("jwt");
    const [isPremiumUser, setIsPremiumUser] = useState(false);

    const clearJwt = () => {
        localStorage.setItem("jwt", "");
    }

    const verifyPremiumUser = async () => {
        if (!token) return;
        const response = await decodeJwt(token);
        if (response["cognito:groups"].includes("premium-user")) {
            setIsPremiumUser(true);
        } else {
            setIsPremiumUser(false);
        }
    }

    const handleUpgrade = async () => {
        if (!token) return;
        const response = await upgradeToPremiumUser(token);

        console.log(response);
    }

    verifyPremiumUser();

    return (
        <nav className='navbar'>
            <NavLink to='/app/portfolio'>
                Dashboard
            </NavLink>
            
            {!isPremiumUser && <button onClick={handleUpgrade}>Upgrade</button>}
            
            <div className="navbar-right">
                <NavLink to='/' onClick={clearJwt}>
                    Log Out
                </NavLink>
            </div>
        </nav>
    )
}

export default NavBar;