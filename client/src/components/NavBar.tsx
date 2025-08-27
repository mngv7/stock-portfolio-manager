import { NavLink } from "react-router-dom";
import '../assets/NavBar.css'

function NavBar() {

    const clearJwt = () => {
        localStorage.setItem("jwt", "");
    }

    return (
        <nav className='navbar'>
            <NavLink to='/app/portfolio'>
                My Portfolio
            </NavLink>
            <NavLink to='/app/trade'>
                Trade
            </NavLink>
            <NavLink to='/app/analysis'>
                Analysis
            </NavLink>
            <div className="navbar-right">
                <NavLink to='/' onClick={clearJwt}>
                    Log Out
                </NavLink>
            </div>
        </nav>
    )
}

export default NavBar;