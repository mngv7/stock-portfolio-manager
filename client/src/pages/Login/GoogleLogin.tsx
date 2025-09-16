const API_URL = import.meta.env.VITE_BUILD_ENV;

function GoogleLogin() {
    const clientId = "1012963124694-v84tliahtescq2oq29kh4vadcjgt1022.apps.googleusercontent.com"
    const loginUri = `https://${API_URL}/auth/google`;

    return(
        <div>
            <script src="https://accounts.google.com/gsi/client" async defer></script>

            <div id="g_id_onload"
                data-client_id={clientId}
                data-login_uri={loginUri}
                data-auto_prompt="false">
            </div>

            <div className="g_id_signin"
                data-type="standard"
                data-shape="rectangular"
                data-theme="outline"
                data-text="signin_with"
                data-size="large">
            </div>
        </div>
    )
}

export default GoogleLogin;