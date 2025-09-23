import { NavLink } from "react-router-dom";
import './NavBar.css'

function NavBar() {

    const clearJwt = () => {
        localStorage.setItem("jwt", "");
    }

    return (
        <nav className='navbar'>
            <NavLink to='/app/portfolio'>
                Dashboard
            </NavLink>
            <button>Upgrade</button>
            <div className="navbar-right">
                <NavLink to='/' onClick={clearJwt}>
                    Log Out
                </NavLink>
            </div>
        </nav>
    )
}

export default NavBar;