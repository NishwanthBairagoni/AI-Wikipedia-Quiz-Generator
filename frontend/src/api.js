import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api', // Adjust if backend port differs
});

export const generateQuiz = (url) => api.post('/generate-quiz', { url });
export const getHistory = () => api.get('/history');
export const getQuiz = (id) => api.get(`/quiz/${id}`);

export default api;
