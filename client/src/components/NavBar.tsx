import { NavLink } from "react-router-dom";
import '../assets/NavBar.css'

function NavBar() {

    const clearJwt = () => {
        localStorage.setItem("jwt", "");
    }

    return (
        <nav className='navbar'>
            <NavLink to='/app/portfolio'>
                Dashboard
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