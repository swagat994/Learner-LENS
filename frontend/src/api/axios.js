import axios from "axios";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});


api.interceptors.request.use(
    (config) => {
        const token =
            localStorage.getItem("token");

        if (token) {
            config.headers.Authorization =
                `Bearer ${token}`;
        }

        if (
            config.data instanceof FormData
        ) {
            delete config.headers["Content-Type"];
        } else {
            config.headers["Content-Type"] =
                "application/json";
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem("token");

            if (
                window.location.pathname !==
                "/login"
            ) {
                window.location.href = "/login";
            }
        }

        return Promise.reject(error);
    }
);


export default api;