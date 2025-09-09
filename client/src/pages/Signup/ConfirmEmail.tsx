import { useState } from "react";
import { confirmEmail } from "../../api/auth";

type SignUpContainerProps = {
    onSuccess: () => void;
    username: string;
};

function ConfirmEmail({onSuccess, username}: SignUpContainerProps) {
    const [confirmationCode, setConfirmationCode] = useState('');

    const handleReturn = () => {
        onSuccess();
    }

    const handleConfirm = async () => {
        if (confirmationCode !== '') {
            const response = await confirmEmail({username, confirmationCode});
            console.log(response);
        } else {
            console.log("Please enter a confirmation code.");
        }
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