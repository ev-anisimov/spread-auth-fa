import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from 'vue'
import {createPinia} from "pinia";
// import axios from "axios";

import App from './App.vue'
import mainRouter from './router/router'
import {useAuthStore} from "@/stores/auth";

const app = createApp(App);
// axios.defaults.withCredentials = true;
// axios.defaults.baseURL = '/api';
// axios.defaults.baseURL = 'http://localhost:5000/';

app.use(mainRouter);
app.use(createPinia())

const authStore = useAuthStore();
authStore.fetchUser();

app.mount('#app')