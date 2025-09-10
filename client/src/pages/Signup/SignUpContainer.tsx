import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { signUp, type SignUpData } from '../../api/auth';
import '../Login/loginContainer.css'

type SignUpContainerProps = {
  onSuccess: () => void;
  setUsernameParent: (username: string) => void;
};

function SignUpContainer({onSuccess, setUsernameParent}: SignUpContainerProps) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [validSignUp, setValidSignUp] = useState(true);
    const navigate = useNavigate();

    const handleBack = () => {
        navigate('/');
    }

    const validateInput = (data: SignUpData, confirmPassword: string): boolean => {
        if (data.password.trim() !== confirmPassword) return false;
        if (!data.username.trim()) return false;
        if (!data.email.trim() || !/\S+@\S+\.\S+/.test(data.email)) return false;
        if (!data.password.trim() || data.password.length < 6) return false;

        return true;
    };

    const handleSignUp = async () => {
        if (validateInput({username, email, password}, confirmPassword )) {
            const response = await signUp({username, email, password});
            console.log(response);
            setUsernameParent(username);

            setUsername('');
            setEmail('');
            setPassword('');
            setConfirmPassword('');
            onSuccess();
            setValidSignUp(true);
        } else {
            setValidSignUp(false);
        }
    }

    return (
        <div className="auth-container sign-up-container">
            <h1 className='login-title'>Sign Up</h1>
            <p className='login-error'>
                {!validSignUp ? "Invalid!" : ""}
            </p>
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
                    type='password'
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    className='login-input'
                    placeholder='Confirm Password'
                    type='password'
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button className='login-button' onClick={handleSignUp}>Sign Up</button>
                <button className='login-button' onClick={handleBack}>Back</button>
            </div>
        </div>
    )
}

export default SignUpContainer;