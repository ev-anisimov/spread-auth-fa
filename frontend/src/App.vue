<template>
  <div id="app">
    <!-- Если пользователь не авторизован, показываем только страницу логина -->
    <LoginView v-if="!authStore.user"/>

    <!-- Если пользователь авторизован -->
    <template v-else>

      <NotificationBox  ref="notificationRef" />
      <div v-if="isHomePage" class="container mt-5">
        <RouterLink :to="{ name: 'users' }" class="btn btn-secondary btn-lg btn-block">
          Администрирование прав
        </RouterLink>
        <RouterLink :to="{ name: 'projector' }" class="btn btn-secondary btn-lg btn-block">
          Настройки сервиса
        </RouterLink>
      </div>

      <div v-else class="d-flex">
        <!-- Боковое меню (только если авторизован) -->
        <div class="col-2">
          <NavMenu/>
        </div>
        <!-- Основной контент -->
        <div class="col-10 p-1 content-area">
          <UserInfo/>
          <RouterView/>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import {computed,  ref, provide} from 'vue';
import {useRoute} from 'vue-router';
import {useAuthStore} from "@/stores/auth";

import NavMenu from '@/components/Permission/NavMenu.vue';
import UserInfo from "@/components/UserInfo.vue";
import LoginView from "@/views/LoginView.vue";
import NotificationBox from "@/components/NotificationBox.vue";


// Доступ к текущему маршруту
const route = useRoute();

const authStore = useAuthStore();
// Проверка, является ли текущая страница домашней
const isHomePage = computed(() => route.path === '/');


// Создаем инстанс уведомлений
// Ссылка на Notification
const notificationRef = ref(null);
provide("notify", (text, type, autoClose) => {
  notificationRef.value?.addMessage(text, type, autoClose);
});
</script>

<style scoped>
#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

div > a {
  display: block;
  margin-top: 5px;
}

.btn {
  margin-top: 5px;
  text-align: center;
}

.d-flex {
  display: flex;
  height: 100%;
}

.col-2 {
  background-color: #111;
  color: #fff;
  min-width: 200px;
}

.col-10 {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.content-area {
  overflow-y: auto; /* Добавлена прокрутка только для этого блока */
  max-height: calc(100vh - 50px); /* Ограничиваем высоту, чтобы прокрутка появилась */
}
</style>
