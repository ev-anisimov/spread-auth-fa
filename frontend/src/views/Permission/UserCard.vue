<template>
  <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <AppBreadcrumbs :items="breadcrumbs" />
      <div>
        <button
          v-if="!isEditing"
          class="btn btn-outline-success me-2"
          @click="toggleEditMode"
        >
          Редактировать
        </button>
        <button
          v-if="isEditing"
          class="btn btn-outline-success me-2"
          @click="saveChanges"
          :disabled="!hasChanges"
        >
          Сохранить
        </button>
        <button class="btn btn-outline-danger" @click="deleteUser">
          Удалить
        </button>
      </div>
    </div>

    <div class="card-body">
      <form @submit.prevent="submitForm">
        <!-- Фамилия -->
        <div class="row mb-3 align-items-center">
          <label class="col-sm-1 col-form-label">Фамилия</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              v-model="localUser.last_name"
              :disabled="!isEditing"
            />
          </div>
        </div>
        <!-- Имя -->
        <div class="row mb-3 align-items-center">
          <label class="col-sm-1 col-form-label">Имя</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              v-model="localUser.first_name"
              :disabled="!isEditing"
            />
          </div>
        </div>
        <!-- Логин -->
        <div class="row mb-3 align-items-center">
          <label class="col-sm-1 col-form-label">Логин</label>
          <div class="col-sm-10">
            <input
              type="text"
              class="form-control"
              v-model="localUser.username"
              :disabled="!isEditing"
            />
          </div>
        </div>
        <!-- Служебный -->
        <div class="row mb-3 align-items-center">
          <label class="col-sm-1 col-form-label">Служебный</label>
          <div class="col-sm-10">
            <input
              type="checkbox"
              class="form-check-input"
              v-model="localUser.is_service"
              :disabled="!isEditing"
            />
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import AppBreadcrumbs from "@/components/AppBreadcrumbs.vue";

const route = useRoute();
const router = useRouter();
const isEditing = ref(false); // Флаг режима редактирования
const hasChanges = ref(false); // Флаг наличия изменений

// Хлебные крошки
const breadcrumbs = ref([
  { label: "Пользователи", url: "/users" },
  { label: "Карточка пользователя", url: "" }, // Это будет заменено
]);

// Данные пользователя из API
const user = reactive({
  id: null,
  updated_at: null,
  username: "",
  first_name: "",
  last_name: "",
  is_service: false,
  is_staff: false,
  name: "",
});

// Локальная копия данных для редактирования
const localUser = reactive({});

// Проверка на изменения
const checkForChanges = () => {
  hasChanges.value = JSON.stringify(user) !== JSON.stringify(localUser);
};

// Загрузка данных пользователя
async function fetchUser() {
  const userId = route.params.id;
  try {
    const response = await axios.get(`/api/v1/users/${userId}`);
    Object.assign(user, response.data);
    Object.assign(localUser, response.data);

    // Обновление хлебных крошек
    breadcrumbs.value[1].label = user.name;
    breadcrumbs.value[1].url =  `/users/${user.id}`;
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  }
}

// Сохранение изменений
async function saveChanges() {
  if (!hasChanges.value) {
    alert("Нет изменений для сохранения.");
    return;
  }
  try {
    const response = await axios.put(`/api/v1/users/${user.id}`, localUser);
    Object.assign(user, response.data); // Обновляем оригинальные данные
    Object.assign(localUser, response.data); // Синхронизируем локальные данные
    hasChanges.value = false; // Сбрасываем флаг изменений
    isEditing.value = false; // Выходим из режима редактирования
    alert("Данные пользователя успешно сохранены!");
  } catch (error) {
    console.error("Ошибка при сохранении данных пользователя:", error);
    alert("Ошибка при сохранении пользователя.");
  }
}

// Включение режима редактирования
function toggleEditMode() {
  isEditing.value = true;
}

// Удаление пользователя
async function deleteUser() {
  if (!confirm("Вы уверены, что хотите удалить пользователя?")) return;
  try {
    await axios.delete(`/api/v1/users/${user.id}`);
    await router.push("/users"); // Редирект на список пользователей
  } catch (error) {
    console.error("Ошибка при удалении пользователя:", error);
    alert("Ошибка при удалении пользователя.");
  }
}

// Следим за изменениями в полях формы
watch(localUser, checkForChanges, { deep: true });

// Загрузка данных при монтировании
onMounted(() => {
  fetchUser();
});
</script>
