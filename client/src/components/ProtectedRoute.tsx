import { useState, useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { isJwtValid } from "../api/auth";

function ProtectedRoute() {
    const token = localStorage.getItem("jwt");
    const [isValid, setIsValid] = useState<boolean | null>(null);

    useEffect(() => {
        const checkToken = async () => {
            if (!token) {
                setIsValid(false);
                return;
            }
            try {
                const valid = await isJwtValid(token);
                setIsValid(valid);
            } catch {
                setIsValid(false);
            }
        };

        checkToken();
    }, [token]);

    if (isValid === null) {
        return <div>Loading...</div>;
    }

    return isValid ? <Outlet /> : <Navigate to="/" replace />;
}

export default ProtectedRoute;
