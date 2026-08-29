import api from "./axios";

export const signup = async (userData) => {
    const response = await api.post(
        "/auth/signup",
        userData
    );

    return response.data;
};

export const login = async (credentials) => {
    const response = await api.post(
        "/auth/login",
        credentials
    );

    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get("/users/me");

    return response.data;
};