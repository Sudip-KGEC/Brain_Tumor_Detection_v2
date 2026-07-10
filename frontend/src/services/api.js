import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    timeout: 60000,
});

export const predictMRI = async (imageFile) => {
    const formData = new FormData();
    formData.append("file", imageFile);
    const response = await API.post("/predict", formData);

    return response.data;
};

export default API;