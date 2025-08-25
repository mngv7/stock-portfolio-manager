const API_URL = 'http://localhost:8080'

export async function isJwtValid(jwt: string) {
    const response = await fetch(`${API_URL}/auth`, {
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
