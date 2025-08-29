const API_URL = import.meta.env.VITE_API_URL;

export interface loginData {
    username: string,
    password: string
}

export async function login(loginData: loginData) {
    const response = await fetch(`${API_URL}/login`, {
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