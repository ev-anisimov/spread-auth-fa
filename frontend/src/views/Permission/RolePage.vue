<template>
  <!--    <RouterView />-->
  <div class="role-page card">
    <ToolBar>
      <template #buttons>
        <AddButton @add-handler="goToNewRole"/>
      </template>
    </ToolBar>
    <div class="header">
      <div class="header-item">Название</div>
      <div class="header-item"></div>
    </div>
    <div class="role-list">
      <RoleRow
          v-for="role in roleList"
          :key="role.id"
          :id="role.id"
          :name="role.name"
          :cnt="role.cnt"
      />
    </div>
  </div>
</template>

<script setup>
import {inject, onMounted, reactive} from "vue";
import {useRouter} from "vue-router";
import axios from "axios";
import AddButton from "@/components/Buttons/AddButton.vue";
import {useAuthStore} from "@/stores/auth";
import RoleRow from "@/components/Permission/RoleRow.vue";
import ToolBar from "@/components/ToolBar.vue";

const authStore = useAuthStore();
var roleList = reactive([]);
const router = useRouter();
const setBreadcrumbs = inject("setBreadcrumbs");

// Функция для перехода в режим создания нового пользователя
const goToNewRole = () => {
  router.push({name: "usercard", params: {id: "new"}}); // Переход без данных
};

onMounted(async () => {
  try {
    let response = await axios.get('api/v1/roles/with_count/', {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    roleList.push(...response.data);
    setBreadcrumbs([]);
  } catch (error) {
    console.error("Ошибка при получении списка ролей:", error);
  }
});
</script>

<style scoped>
/* Общая обёртка для страницы пользователей */
.role-page {
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
.role-list {
  display: flex;
  flex-direction: column;
}

.role-row > div {
  padding: 0 10px;
  display: flex;
  align-items: center; /* Вертикальное выравнивание */
}
</style>