import axios from "axios";
import { useAuthStore } from "./stores/auth";

const api = axios.create({
  baseURL: "/api",
});

// Добавляем токен в заголовки запросов
api.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

export default api;
