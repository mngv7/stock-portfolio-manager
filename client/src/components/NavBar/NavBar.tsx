import { NavLink } from "react-router-dom";
import './NavBar.css'
import { upgradeToPremiumUser } from "../../api/auth";

function NavBar() {
    const token = localStorage.getItem("jwt");

    const clearJwt = () => {
        localStorage.setItem("jwt", "");
    }

    const handleUpgrade = async () => {
        if (!token) return;
        const response = await upgradeToPremiumUser(token);

        console.log(response);
    }

    return (
        <nav className='navbar'>
            <NavLink to='/app/portfolio'>
                Dashboard
            </NavLink>
            <button onClick={handleUpgrade}>Upgrade</button>
            <div className="navbar-right">
                <NavLink to='/' onClick={clearJwt}>
                    Log Out
                </NavLink>
            </div>
        </nav>
    )
}

export default NavBar;