import { useState } from "react";
import { confirmEmail } from "../../api/auth";
import { useNavigate } from "react-router-dom";

type SignUpContainerProps = {
    onSuccess: () => void;
    username: string;
};

function ConfirmEmail({onSuccess, username}: SignUpContainerProps) {
    const [confirmationCode, setConfirmationCode] = useState('');
    const navigate = useNavigate();

    const handleReturn = () => {
        onSuccess();
    }

    const handleConfirm = async () => {
        if (confirmationCode !== '') {
            const response = await confirmEmail({username, confirmationCode});
            if (!response) {
                console.log("Invalid verification code!");
            } else {
                console.log()
                navigate('/');
            }
            console.log(response);
        } else {
            console.log("Please enter a confirmation code.");
        }
    }

    return (
        <div className="auth-container login-container">
            <h1>Confirm Email</h1>
            <button onClick={handleReturn}>Return</button>
            <div className='login-input-button-group'>
                <input
                    className="login-input"
                    placeholder="Confirmation Code"
                    value={confirmationCode}
                    onChange={(e) => setConfirmationCode(e.target.value)}
                />
                <button className="login-button" onClick={handleConfirm}>Confirm</button>
            </div>
        </div>
    )
}

export default ConfirmEmail;