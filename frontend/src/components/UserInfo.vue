<template>
  <div class="user-info">
    <span>Добро пожаловать, <strong>{{ user?.first_name }}</strong></span> |
    <a href="#" @click.prevent="logout" class="logout">Выход</a>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth"; // Храним юзера в Pinia
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const user = computed(() => authStore.user);

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<style scoped>
.user-info {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  background-color: #f8f9fa;
}

.logout {
  color: blue;
  cursor: pointer;
  text-decoration: none;
}

.logout:hover {
  text-decoration: underline;
}
</style>
