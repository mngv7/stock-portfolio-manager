// TypeScript file
// @ts-ignore
import fetchParameterLocal from '../utils/parameterStore'

const API_URL = await fetchParameterLocal(`/n11592931/prod/${import.meta.env.VITE_BUILD_ENV}/api_url`);

export interface LoginData {
    username: string,
    password: string
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
    const response = await fetch(`${API_URL}/api/v2/auth`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${jwt}`
        },
    });

    if (!response.ok) {
        return false;
    }

    return true;
}

export async function login(loginData: LoginData) {
    console.log(API_URL);
    const response = await fetch(`${API_URL}/api/v2/login`, {
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

export async function signUp(signUpData: SignUpData) {
    const response = await fetch(`${API_URL}/api/v1/signup`, {
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
    const response = await fetch(`${API_URL}/api/v1/confirm_email`, {
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