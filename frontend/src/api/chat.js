import api from "./axios";

export const sendMessage = async (
    courseId,
    message
) => {
    const response = await api.post(
        `/courses/${courseId}/chat`,
        {
            message,
        }
    );

    return response.data;
};


export const getChatHistory = async (
    courseId
) => {
    const response = await api.get(
        `/courses/${courseId}/chat`
    );

    return response.data;
};