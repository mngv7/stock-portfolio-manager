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
                navigate('/app/')
            }
        } catch (err) {
            setShowLoginFailed(true);
        }
    };

    return (
        <div className='login-container'>
            <h1>Login</h1>
            <p style={{ color: 'red', marginTop: '10px', minHeight: '20px' }}>
                {showLoginFailed ? "Login Failed!" : ""}
            </p>
            <div className='input-button-group'>
                <input 
                    placeholder='Username'
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    placeholder='Password'
                    onChange={(e) => setPassword(e.target.value)}
                    type='password'
                />
                <button onClick={handleLogin}>Login</button>
            </div>
        </div>
    )
}

export default LoginContainer