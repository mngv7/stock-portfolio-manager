import { useState } from "react";

type SignUpContainerProps = {
    onSuccess: () => void
};

function ConfirmEmail({onSuccess}: SignUpContainerProps) {
    const [confirmationCode, setConfirmationCode] = useState('');

    const handleReturn = () => {
        onSuccess();
    }

    const handleConfirm = () => {
        // check confirmation code here
    }

    return (
        <div className="auth-container login-container">
            <h1>Confirm Email</h1>
            <div className='login-input-button-group'>
                <input
                    className="login-input"
                    placeholder="Confirmation Code"
                    value={confirmationCode}
                    onChange={(e) => setConfirmationCode(e.target.value)}
                />
                <button className="login-button" onClick={handleConfirm}>Confirm</button>
                <button className="login-button" onClick={handleReturn}>Return</button>
            </div>
        </div>
    )
}

export default ConfirmEmail;