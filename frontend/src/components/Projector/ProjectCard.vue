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
        <!-- Ид проекта -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.project_id}">
          <label class="col-sm-1 col-form-label">Ид проекта</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.project_id"
                :disabled="!isEditing"
            />
            <small v-if="errors.project_id" class="error-text">{{ errors.project_id }}</small>
          </div>
        </div>
        <!-- Название -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.name}">
          <label class="col-sm-1 col-form-label">Название</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.name"
                :disabled="!isEditing"
            />
            <small v-if="errors.name" class="error-text">{{ errors.name }}</small>
          </div>
        </div>
        <!-- Тип -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.type}">
          <label class="col-sm-1 col-form-label">Тип</label>
          <div class="col-sm-10">
            <select v-model="localObject.type" class="form-control" :disabled="!isEditing">
              <option v-for="type in types" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
            <small v-if="errors.type" class="error-text">{{ errors.type }}</small>
          </div>
        </div>

        <!-- Данные подключения -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.type}">
          <label class="col-sm-1 col-form-label">Данные подключения</label>
          <!-- Spread -->
          <div v-if="localObject.type=='spread'" class="mb-3 align-items-center">
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Хост</label>
              <div class="col-sm-10">
                <input type="text" class="form-control"
                       :disabled="!isEditing"
                       v-model="localObject.connection_params.host"/>
              </div>
            </div>
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Порт</label>
              <div class="col-sm-10">
                <input type="number" class="form-control" maxlength="30" :disabled="!isEditing"
                       v-model="localObject.connection_params.port"/>
              </div>
            </div>
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Вебпорт</label>
              <div class="col-sm-10">
                <input type="number" class="form-control" pattern="\d*" maxlength="30"
                       :disabled="!isEditing"
                       v-model="localObject.connection_params.webport"/>
              </div>
            </div>
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">SSL</label>
              <div class="col-sm-10">
                <input type="checkbox" :disabled="!isEditing" v-model="localObject.connection_params.ssl"/>
              </div>
            </div>
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Логин</label>
              <div class="col-sm-10">
                <input type="text" :disabled="!isEditing" class="form-control" maxlength="30"
                       v-model="localObject.connection_params.login"/>
              </div>
            </div>
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Пароль</label>
              <div class="col-sm-10">
                <input type="password" :disabled="!isEditing" class="form-control" maxlength="30"
                       v-model="localObject.connection_params.password"/>
              </div>
            </div>
            <small v-if="errors.type" class="error-text">{{ errors.type }}</small>
          </div>
          <!-- Cloud -->
          <div v-if="localObject.type=='cloud'" class="mb-3 align-items-center">
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Код</label>
              <div class="col-sm-10">
                <input type="text" :disabled="!isEditing" class="form-control"
                       v-model="localObject.connection_params.code"
                       placeholder="dddd-dddd-dddd" pattern="\d{4}-\d{4}-\d{4}"/>
              </div>
            </div>
          </div>
          <!-- Custom -->
          <div v-if="localObject.type=='custom'" class="mb-3 align-items-center">
            <div class="row mb-3">
              <label class="col-sm-1 col-form-label">Данные</label>
              <div class="col-sm-10">
                <input type="text" :disabled="!isEditing" class="form-control"
                       v-model="localObject.connection_params.data"/>
              </div>
            </div>
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
const types = [
  {id: 'spread', name: 'Spread'},
  {id: 'cloud', name: 'Cloud'},
  {id: 'custom', name: 'Custom'},
]
//
// const props = defineProps({
//   type
// });

// Данные пользователя из API
const dbObject = reactive({
  id: null,
  updated_at: null,
  name: "",
  type: "",
  connection_params: {},
});

// Локальная копия данных для редактирования
const localObject = reactive({
  id: null,
  updated_at: null,
  name: "",
  type: "",
  connection_params: {},
});

const errors = ref({}); // Ошибки валидации

// Проверка на изменения
const checkForChanges = () => {
  hasChanges.value = JSON.stringify(dbObject) !== JSON.stringify(localObject);
};

// Загрузка данных пользователя
async function fetchProject() {
  const userId = route.params.id;
  try {
    const response = await axios.get(`/api/v1/projects/${userId}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    Object.assign(dbObject, response.data);
    Object.assign(localObject, response.data);

    // Парсим `connection_params` (из строки в объект)
    localObject.connection_params = JSON.parse(response.data.connection_params || "{}");

    setBreadcrumbs([
      {label: "Проекты", url: "/projects/"},
      {label: dbObject.name, url: `/projects/${dbObject.id}`},
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
    let response;
    const payload = {...localObject, connection_params: JSON.stringify(localObject.connection_params)};
    if (!payload.password) delete payload.password;

    if (isNew.value) {
      response = await axios.post("/api/v1/projects", payload, {
        headers: {Authorization: `Bearer ${authStore.token}`}
      });
    } else {
      response = await axios.put(`/api/v1/projects/${dbObject.id}`, payload, {
        headers: {Authorization: `Bearer ${authStore.token}`}
      });
    }
    Object.assign(dbObject, response.data); // Обновляем оригинальные данные
    Object.assign(localObject, response.data); // Синхронизируем локальные данные
    localObject.connection_params = JSON.parse(response.data.connection_params || "{}");
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
    fetchProject();
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