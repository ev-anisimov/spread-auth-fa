import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      try {
        let data = new FormData()
        data.append('username',username)
        data.append('password',password)
        const response = await axios.post("/api/login", data, { headers: { 'content-type': 'application/x-www-form-urlencoded' } } );
        this.token = response.data.access_token;
        localStorage.setItem("token", this.token);

        await this.fetchUser(); // Загружаем текущего пользователя
      } catch (error) {
        console.error("Ошибка входа:", error);
        throw error;
      }
    },

    async fetchUser() {
      if (!this.token) return;

      try {
        const response = await axios.get("/api/user", {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.user = response.data;
      } catch (error) {
        console.error("Ошибка загрузки пользователя:", error);
        this.logout();
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
    },
  },
});
