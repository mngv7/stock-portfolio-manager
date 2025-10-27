export interface LoginData {
    username: string,
    password: string
}

export interface ChallengeData {
    username: string,
    authCode: string,
    session: string
}

export interface SignUpData {
    username: string,
    email: string,
    password: string
    phoneNumber: string
}

export interface ConfirmEmailData {
    username: string,
    confirmationCode: string
}

export async function isJwtValid(jwt: string) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v2/auth`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${jwt}`
        },
    });

    if (!response.ok) {
        return false;
    }

    return true;
}

export async function login(loginData: LoginData) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v2/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
    });

    if (!response.ok) {
        const error = new Error("Login failed") as any;
        error.status = response.status;
        throw error;
    }

    return response.json();
}

export async function emailOtpChallenge(challengeData: ChallengeData) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v1/challenge_response`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(challengeData)
    });

    if (!response.ok) {
        const error = new Error("Login failed") as any;
        error.status = response.status;
        throw error;
    }

    return response.json();
}

export async function signUp(signUpData: SignUpData) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v1/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(signUpData)
    });

    if (!response.ok) {
        const error = new Error("Signup failed!") as any;
        error.status = response.status;
        throw error;
    }

    return response.json();
}


export async function confirmEmail(confirmEmailData: ConfirmEmailData) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v1/confirm_email`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(confirmEmailData)
    });

    if (!response.ok) {
        const error = new Error("Failed to confirm email!") as any;
        error.status = response.status;
        throw error;
    }

    return response.json();
}

export async function decodeJwt(jwt: string) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v1/jwt/decode`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`
        }
    });

    if (!response.ok) {
        return response.status;
    }

    return response.json();
}

export async function upgradeToPremiumUser(jwt: string) {
    const response = await fetch(`https://api.portfoliomanager.cab432.com/v1/api/v1/user/group`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`
        },
        body: JSON.stringify({ group: "premium-user" })
    });

    if (!response.ok) {
        const error = new Error("Failed to upgrade user to premium!") as any;
        error.status = response.status;
        throw error;
    }

    return response.json();
}
