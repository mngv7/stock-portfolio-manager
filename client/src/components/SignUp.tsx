import { useNavigate } from 'react-router-dom';
import '../assets/loginContainer.css'
import { useState } from 'react';

function SignUp() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const navigate = useNavigate();

    const handleBack = () => {
        navigate('/');
    }

    const handleSignUp = async () => {
        // call a signup endpoint here.
    }

    return (
        <div className="auth-container sign-up-container">
            <h1 className='login-title'>Sign Up</h1>
            <div className='login-input-button-group'>
                <input
                    className='login-input'
                    placeholder='Email Address'
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    className='login-input'
                    placeholder='Username'
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    className='login-input'
                    placeholder='Password'
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    className='login-input'
                    placeholder='Confirm Password'
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button className='login-button' onClick={handleSignUp}>Sign Up</button>
                <button className='login-button' onClick={handleBack}>Back</button>
            </div>
        </div>
    )
}

export default SignUp;