<template>
  <div class="container mt-5 min-width">
    <div class="logo mx-auto">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1620.47 156.49" class="mt-2">
        <path class="a"
              d="M647.86,168.21H605.81L532.73,55.55,532.31,34l-9.56,15.41-77,118.75H408.58L307.1,11.79H350l77.19,119,77.19-119h42.86l77.19,119,82.11-119h42.86L647.86,168.21ZM148.51,11.79H111.39L9.91,168.21H52.76l55.86-86.14,29.55-48.59.38,29,68.59,105.76H250L148.51,11.79Zm798.07,0H909.45L808,168.21h42.86l55.86-86.14,29.55-48.59.38,29,68.59,105.76h42.86L946.58,11.79Zm582.31,0h-37.12L1390.29,168.21h42.86L1489,82.07l29.55-48.59.38,29,68.59,105.76h42.85L1528.89,11.79ZM1123.6,150.9v17.31l127.49.05c1,.06,2.2-.08,3.44-.06s2.39-.16,3.59-.19a74.8,74.8,0,0,0,23.34-4.28,57.06,57.06,0,0,0,18.91-11,50.79,50.79,0,0,0,12.2-16,51.4,51.4,0,0,0,5-19.33h.13V80.74a75.66,75.66,0,0,0-4.86-26.85,66.36,66.36,0,0,0-13.91-22.23,61.71,61.71,0,0,0-21.32-14.58,68.38,68.38,0,0,0-26.19-4.94l-127.81-.08V150.9Zm37-89.13V60.16l-18.48-13.6c32.17,0,77.11,0,109.28,0a35,35,0,0,1,12.86,2.26,27.07,27.07,0,0,1,9.76,6.51,31.87,31.87,0,0,1,6.78,11.12,41.5,41.5,0,0,1,2.44,14.27v33.07l.07.33c0,.45-.08,1-.05,1.43a16.86,16.86,0,0,1-1.63,6.24,16.43,16.43,0,0,1-4,5.24,23.43,23.43,0,0,1-8.33,4.57,41.24,41.24,0,0,1-11.86,1.86h-2.25c-30.39-1.2-63.86.5-94.58.8V61.77Z"
              transform="translate(-9.91 -11.79)"/>
      </svg>
    </div>
    <hr>
    <form @submit.prevent="handleLogin" method="post" class="mt-5">
      <div class="form-group row">
        <div class="col-sm-1 col-form-label">
          <label for="username">Логин:</label>
        </div>
        <div class="col-sm">
          <input
              id="username"
              v-model="username"
              type="text"
              class="input-field"
              required
          />
        </div>
      </div>

      <div class="form-group row">
        <div class="col-sm-1 col-form-label">
          <label for="password">Пароль:</label>
        </div>
        <div class="col-sm">
          <input
              id="password"
              v-model="password"
              type="password"
              class="input-field"
              required
          />
        </div>
      </div>

      <button type="submit" class="btn btn-outline-success d-block mx-auto">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {useAuthStore} from "../stores/auth";
import {useRouter} from "vue-router";

const username = ref("");
const password = ref("");
const error = ref(null);
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    error.value = null;
    await authStore.login(username.value, password.value);
    router.push("/"); // Редирект после успешного входа
  } catch (e) {
    error.value = "Ошибка авторизации";
  }
}
</script>

<style scoped>

.container{
  width: 35%;
}
.form-group {
  margin-bottom: 1rem;
}

.logo{
  width: 45rem;
  text-align: center;
}

.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
