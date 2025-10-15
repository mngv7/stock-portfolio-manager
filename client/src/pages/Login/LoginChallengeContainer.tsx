import { useState } from 'react'
import { emailOtpChallenge } from '../../api/auth'
import '../Login/LoginContainer.css'
import { useNavigate } from 'react-router-dom'
import LoginContainer from './LoginContainer'

interface LoginChallengeProps {
    username: string
    session: string
}

function LoginChallengeContainer({ username, session }: LoginChallengeProps) {
    const [authCode, setAuthCode] = useState('');
    const [_, setInvalidCode] = useState(false);
    const [returnToLogin, setReturnToLogin] = useState(false);
    const navigate = useNavigate();

    const isCodeValid = (code: string) => {
        const regex = /^\d{6}$/;
        return regex.test(code);
    }

    const handleChallengeAttempt = async () => {
        if (isCodeValid(authCode)) {
            const challengeData = {
                username: username,
                authCode: authCode,
                session: session
            }
            const response = await emailOtpChallenge(challengeData);
            const id_token = response.id_token;
            if (id_token) {
                localStorage.setItem('jwt', id_token);
                navigate('/app/portfolio');
            }
        } else {
            setInvalidCode(true);
        }
    }

    const handleReturn = () => {
        setReturnToLogin(true);
    }

    if (returnToLogin) {
        return <LoginContainer />
    }

    return (
        <div className='auth-container challenge-container'>
            <h1>MFA</h1>
            <div className='login-input-button-group'>
                <input
                    value={authCode}
                    onChange={(e) => setAuthCode(e.target.value)}
                    className='login-input'
                    placeholder="MFA Code"
                />
                <button
                    className='login-button'
                    onClick={handleChallengeAttempt}
                    disabled={!isCodeValid(authCode)}
                >
                    Confirm
                </button>
                <button className='login-button' onClick={handleReturn}>Return</button>
            </div>
        </div>
    );

}

export default LoginChallengeContainer;