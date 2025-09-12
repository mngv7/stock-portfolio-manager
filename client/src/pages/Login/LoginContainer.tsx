import { useState } from 'react'
import './LoginContainer.css'
import { login } from '../../api/auth';
import { useNavigate } from 'react-router-dom';
import LoginChallengeContainer from './LoginChallengeContainer';

function LoginContainer() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showLoginFailed, setShowLoginFailed] = useState(false);
    const [session, setSession] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async () => {
        const loginData = {
            username,
            password
        };

        try {
            const response = await login(loginData);
            if (response.ChallengeName) {
                setSession(response.Session);
            }
        } catch (err) {
            setShowLoginFailed(true);
        }
    };

    const handleSignUp = () => {
        navigate('/signup')
    };

    if (session){
        return (
            <LoginChallengeContainer username={username} session={session}/>
        )
    }

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
