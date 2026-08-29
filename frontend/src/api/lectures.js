import api from "./axios";


export const getLectures = async (
    courseId
) => {
    const response = await api.get(
        `/courses/${courseId}/lectures`
    );

    return response.data;
};


export const uploadLecture = async (
    courseId,
    title,
    file
) => {
    const formData = new FormData();

    formData.append("title", title);
    formData.append("file", file);

    const response = await api.post(
        `/courses/${courseId}/lectures`,
        formData
    );

    return response.data;
};


export const getLecture = async (
    courseId,
    lectureId
) => {
    const response = await api.get(
        `/courses/${courseId}/lectures/${lectureId}`
    );

    return response.data;
};


export const summarizeLecture = async (
    courseId,
    lectureId
) => {
    const response = await api.post(
        `/courses/${courseId}/lectures/${lectureId}/summarize`
    );

    return response.data;
};


export const generateQuiz = async (
    courseId,
    lectureId
) => {
    const response = await api.post(
        `/courses/${courseId}/lectures/${lectureId}/quiz`
    );

    return response.data;
};


export const generateFlashcards = async (
    courseId,
    lectureId
) => {
    const response = await api.post(
        `/courses/${courseId}/lectures/${lectureId}/flashcards`
    );

    return response.data;
};