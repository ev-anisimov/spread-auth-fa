<template>
  <div class="card">

      <ToolBar>
        <template #buttons>
          <EditButton v-if="!isEditing" @click-handler="toggleEditMode"/>
          <SaveButton v-if="isEditing" @click-handler="saveChanges" :has-changes="hasChanges"
                      :is-new="isNew"/>
          <DeleteButton @click="deleteUser"/>
        </template>
      </ToolBar>

    <div class="card-body">
      <form @submit.prevent="submitForm">
        <!-- Фамилия -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.last_name}">
          <label class="col-sm-1 col-form-label">Фамилия</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.last_name"
                :disabled="!isEditing"
            />
            <small v-if="errors.last_name" class="error-text">{{ errors.last_name }}</small>

          </div>
        </div>
        <!-- Имя -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.first_name}">
          <label class="col-sm-1 col-form-label">Имя</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.first_name"
                :disabled="!isEditing"
            />
            <small v-if="errors.first_name" class="error-text">{{ errors.first_name }}</small>
          </div>
        </div>
        <!-- Логин -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.username}">
          <label class="col-sm-1 col-form-label">Логин</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.username"
                :disabled="!isEditing"
            />
            <small v-if="errors.username" class="error-text">{{ errors.username }}</small>

          </div>
        </div>
        <!-- Пароль -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.password}">
          <label class="col-sm-1 col-form-label">Пароль</label>
          <div class="col-sm-10">
            <input
                type="password"
                class="form-control"
                v-model="localObject.password"
                :disabled="!isEditing"
            />
            <small v-if="errors.password" class="error-text">{{ errors.password }}</small>
          </div>
        </div>

        <!-- Служебный -->
        <div class="row mb-3 align-items-center">
          <label class="col-sm-1 col-form-label">Служебный</label>
          <div class="col-sm-10">
            <input
                type="checkbox"
                class="form-check-input"
                v-model="localObject.is_service"
                :disabled="!isEditing"
            />
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {onMounted, computed, reactive, ref, watch, inject} from "vue";
import {useRoute, useRouter} from "vue-router";
import axios from "axios";
import {useAuthStore} from "@/stores/auth";
import EditButton from "@/components/Buttons/EditButton.vue";
import SaveButton from "@/components/Buttons/SaveButton.vue";
import DeleteButton from "@/components/Buttons/DeleteButton.vue";
import ToolBar from "@/components/ToolBar.vue";

const route = useRoute();
const router = useRouter();
const hasChanges = ref(false);
const authStore = useAuthStore();
const notify = inject("notify");
const setBreadcrumbs = inject("setBreadcrumbs");
const isNew = computed(() => route.params.id === "new");
const isEditing = ref(isNew.value);


// Данные пользователя из API
const dbObject = reactive({
  id: null,
  updated_at: null,
  username: "",
  name: "",
  first_name: "",
  last_name: "",
  is_service: false,
  is_staff: false,
  password: ""
});

// Локальная копия данных для редактирования
const localObject = reactive({
  id: null,
  updated_at: null,
  username: "",
  name: "",
  first_name: "",
  last_name: "",
  is_service: false,
  is_staff: false,
  password: ""
});

const errors = ref({}); // Ошибки валидации

// Проверка на изменения
const checkForChanges = () => {
  hasChanges.value = JSON.stringify(dbObject) !== JSON.stringify(localObject);
};

// Загрузка данных пользователя
async function fetchData() {
  const userId = route.params.id;
  try {
    const response = await axios.get(`/api/v1/users/${userId}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    Object.assign(dbObject, response.data);
    Object.assign(localObject, response.data);
    setBreadcrumbs([
      {label: "Пользователи", url: "/users"},
      {label: dbObject.name, url: `/users/${dbObject.id}`},
    ]);
  } catch (error) {
    notify(`Ошибка при получении данных пользователя ${error}`, "error", false);
  }
}

// Сохранение изменений
async function saveChanges() {
  if (!hasChanges.value) {
    notify("Нет изменений для сохранения.", "warning");
    return;
  }
  try {
    let response
    const payload = {...localObject};
    if (!payload.password) delete payload.password;

    if (isNew.value) {
      response = await axios.post("/api/v1/users", payload, {
        headers: {Authorization: `Bearer ${authStore.token}`}
      });
    } else {
      response = await axios.put(`/api/v1/users/${dbObject.id}`, payload, {
        headers: {Authorization: `Bearer ${authStore.token}`}
      });
    }
    Object.assign(dbObject, response.data); // Обновляем оригинальные данные
    Object.assign(localObject, response.data); // Синхронизируем локальные данные
    hasChanges.value = false; // Сбрасываем флаг изменений
    isEditing.value = false; // Выходим из режима редактирования
    notify("Изменения сохранены", "success");
    errors.value = {};

  } catch (error) {
    if (error.response && error.response.data.detail) {
      const detail = error.response.data.detail;

      if (Array.isArray(detail)) {
        // Если `detail` — массив, разбираем ошибки
        errors.value = parseValidationErrors(detail);
      } else if (typeof detail === "string") {
        // Если `detail` — строка (например, "403: Access denied"), показываем как уведомление
        notify(detail, "error", false);
      } else {
        notify("Ошибка при сохранении пользователя", "error", false);
      }
    } else {
      notify("Ошибка при сохранении пользователя", "error", false);
    }
  }
}

function parseValidationErrors(detail) {
  const parsedErrors = {};
  detail.forEach(err => {
    if (err.loc && err.loc.length > 1) {
      const field = err.loc[1]; // Берём название поля из `loc`
      parsedErrors[field] = err.msg; // Сообщение об ошибке
    }
  });
  return parsedErrors;
}

// Включение режима редактирования
function toggleEditMode() {
  isEditing.value = true;
}

// Удаление пользователя
async function deleteUser() {
  if (!confirm("Вы уверены, что хотите удалить пользователя?")) return;
  try {
    await axios.delete(`/api/v1/users/${dbObject.id}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    await router.push("/users"); // Редирект на список пользователей
  } catch (error) {
    notify(`Ошибка при удалении пользователя ${error}`, "error", false);
  }
}

// Следим за изменениями в полях формы
watch(localObject, checkForChanges, {deep: true});

// Загрузка данных при монтировании
onMounted(() => {
  if (!isNew.value) {
    fetchData();
  }

});
</script>
<style scoped>
.has-error .form-control {
  border-color: #dc3545;
}

.error-text {
  color: #dc3545;
  font-size: 12px;
}
</style>