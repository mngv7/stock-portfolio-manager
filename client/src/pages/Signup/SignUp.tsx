import { useState } from 'react';
import '../Login/LoginContainer.css'
import SignUpContainer from './SignUpContainer';
import ConfirmEmail from './ConfirmEmail';

function SignUp() {
    const [showConfirmation, setShowConfirmation] = useState(false);

    if (showConfirmation) {
        return (
            <div className="signup-page">
                <ConfirmEmail onSuccess={() => setShowConfirmation(false)} />
            </div>
        )    
    }
    return (
        <div className="signup-page">
            <SignUpContainer onSuccess={() => setShowConfirmation(true)} />
        </div>
    )
}

export default SignUp;