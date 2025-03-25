import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Используем прокси из vue.config.js
  withCredentials: true, // Для передачи кук с авторизацией
  headers: {
    'Content-Type': 'application/json',
  }
});

export default api;
