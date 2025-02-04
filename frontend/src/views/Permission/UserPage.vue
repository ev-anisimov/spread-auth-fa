<template>
  <!--    <RouterView />-->
  <div class="user-page">
    <div class="header">
      <AddButton @add-handler="goToNewUser" />
      <div class="header-item">ФИО</div>
      <div class="header-item">Логин</div>
    </div>
    <div class="user-list">
      <UserRow
          v-for="user in userList"
          :key="user.id"
          :id="user.id"
          :full-name="user.name"
          :username="user.username"
      />
    </div>
  </div>
</template>

<script setup>
import {onMounted, reactive} from "vue";
import { useRouter } from "vue-router";
import UserRow from "@/components/Permission/UserRow.vue";
import axios from "axios";
import AddButton from "@/components/AddButton.vue";
import {useAuthStore} from "@/stores/auth";

const authStore = useAuthStore();
var userList = reactive([]);
const router = useRouter();

// Функция для перехода в режим создания нового пользователя
const goToNewUser = () => {
  router.push({ name: "usercard", params: { id: "new" } }); // Переход без данных
};

onMounted(async () => {
  try {
    const response = await axios.get('api/v1/users', {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    userList.push(...response.data);
  } catch (error) {
    console.error("Ошибка при получении списка пользователей:", error);
  }
});
</script>

<style scoped>
/* Общая обёртка для страницы пользователей */
.user-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}

/* Заголовки */
.header {
  display: grid;
  grid-template-columns: 2fr 1fr; /* 2 части для ФИО, 1 часть для логина */
  position: sticky;
  top: 0;
  background-color: #f8f9fa;
  z-index: 1;
  border-bottom: 1px solid #dee2e6;
  padding: 10px 0;
  font-weight: bold;
  text-align: left;
}

.header-item {
  padding: 0 10px;
  text-align: left;
}

/* Список пользователей */
.user-list {
  display: flex;
  flex-direction: column;
}

/* Строка пользователя */
.user-row {
  display: grid;
  grid-template-columns: 2fr 1fr; /* Соответствует заголовкам */
  padding: 10px 0 10px 5px;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.user-row:hover {
  background-color: #f1f3f5;
}

.user-row > div {
  padding: 0 10px;
  display: flex;
  align-items: center; /* Вертикальное выравнивание */
}
</style>