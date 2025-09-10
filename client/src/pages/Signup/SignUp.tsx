import { useState } from 'react';
import '../Login/LoginContainer.css'
import SignUpContainer from './SignUpContainer';
import ConfirmEmail from './ConfirmEmail';

function SignUp() {
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [username, setUsername] = useState('');

    if (showConfirmation) {
        return (
            <div className="signup-page">
                <ConfirmEmail
                    onSuccess={() => setShowConfirmation(false)}
                    username={username}
                />
            </div>
        )    
    }
    return (
        <div className="signup-page">
            <SignUpContainer
                onSuccess={() => setShowConfirmation(true)}
                setUsernameParent={setUsername}
            />
        </div>
    )
}

export default SignUp;