<template>
  <!--    <RouterView />-->
  <div class="page card">
    <ToolBar>
        <template #buttons>
         <AddButton @add-handler="goToNewUser" />
        </template>
      </ToolBar>
    <div class="header">
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
import {inject, onMounted, reactive} from "vue";
import { useRouter } from "vue-router";
import UserRow from "@/components/Permission/UserRow.vue";
import api from "@/api/axiosConfig";
import AddButton from "@/components/Buttons/AddButton.vue";
import {useAuthStore} from "@/stores/auth";
// import EditButton from "@/components/Buttons/EditButton.vue";
// import SaveButton from "@/components/Buttons/SaveButton.vue";
// import DeleteButton from "@/components/Buttons/DeleteButton.vue";
import ToolBar from "@/components/ToolBar.vue";

const authStore = useAuthStore();
var userList = reactive([]);
const router = useRouter();
const setBreadcrumbs = inject("setBreadcrumbs");

// Функция для перехода в режим создания нового пользователя
const goToNewUser = () => {
  router.push({ name: "usercard", params: { id: "new" } }); // Переход без данных
};

onMounted(async () => {
  try {
    const response = await api.get('/v1/users/', {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    userList.push(...response.data);
    setBreadcrumbs([]);
  } catch (error) {
    console.error("Ошибка при получении списка пользователей:", error);
  }
});
</script>

<style scoped>
/* Общая обёртка для страницы пользователей */
.page {
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


.user-row > div {
  padding: 0 10px;
  display: flex;
  align-items: center; /* Вертикальное выравнивание */
}
</style>