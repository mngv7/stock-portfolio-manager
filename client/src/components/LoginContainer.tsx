import { useState } from 'react'
import '../assets/loginContainer.css'
import { login } from '../api/login';
import { useNavigate } from 'react-router-dom';

function LoginContainer() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showLoginFailed, setShowLoginFailed] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async () => {
        const loginData = {
            username,
            password
        };

        try {
            const response = await login(loginData);

            if (response?.authToken) {
                localStorage.setItem('jwt', response.authToken);
                setShowLoginFailed(false);
                navigate('/app/portfolio')
            }
        } catch (err) {
            setShowLoginFailed(true);
        }
    };

    const handleSignUp = () => {
        navigate('/signup')
    };

    return (
        <div className='auth-container login-container'>
            <h1 className='login-title'>Login</h1>
            <p className='login-error'>
                {showLoginFailed ? "Login Failed!" : ""}
            </p>
            <div className='login-input-button-group'>
                <input 
                    className='login-input'
                    placeholder='Username'
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    className='login-input'
                    placeholder='Password'
                    onChange={(e) => setPassword(e.target.value)}
                    type='password'
                />
                <button className='login-button' onClick={handleLogin}>
                    Login
                </button>
                <button className='login-button' onClick={handleSignUp}>
                    Sign Up
                </button>
            </div>
        </div>
    )
}

export default LoginContainer
