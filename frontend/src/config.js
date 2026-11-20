export default function getEnvData() {


    return {
        BACKEND_API_URL: import.meta.env.VITE_BACKEND_API_MAIN_URL,
        LS_USER_INFO_KEY: import.meta.env.VITE_LS_USER_INFO_KEY,
        LS_SESSION: import.meta.env.VITE_LS_SESSION_KEY,
    }
}