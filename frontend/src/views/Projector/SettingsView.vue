<template>
  <div class="card">
    <ToolBar>
      <template #buttons>
        <SaveButton @click-handler="saveChanges" :has-changes="hasChanges"
                    :is-new="isNew"/>
        <BaseButton @click-handler="loadEntity"
                    title="Загрузить EQ"
                    has-changes="true"
                    btn-cls="btn-outline-info"/>
      </template>
    </ToolBar>

    <div class="card-body">
      <form @submit.prevent="submitForm">
        <!-- Название -->
        <div class="row mb-3 align-items-center" :class="{'has-error': errors.name}">
          <label class="col-sm-1 col-form-label">Название</label>
          <div class="col-sm-10">
            <input
                type="text"
                class="form-control"
                v-model="localObject.name"
            />
            <small v-if="errors.name" class="error-text">{{ errors.name }}</small>

          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref, watch, inject} from "vue";
import api from "@/api/axiosConfig";
import {useAuthStore} from "@/stores/auth";
import SaveButton from "@/components/Buttons/SaveButton.vue";
import ToolBar from "@/components/ToolBar.vue";
import BaseButton from "@/components/Buttons/BaseButton.vue";

const hasChanges = ref(false);
const authStore = useAuthStore();
const notify = inject("notify");
const setBreadcrumbs = inject("setBreadcrumbs");


// Данные пользователя из API
const dbObject = reactive({
  name: "",
});

// Локальная копия данных для редактирования
const localObject = reactive({
  name: "",
});

const errors = ref({}); // Ошибки валидации

// Проверка на изменения
const checkForChanges = () => {
  hasChanges.value = JSON.stringify(dbObject) !== JSON.stringify(localObject);
};

// Загрузка данных пользователя
async function fetchData() {
  try {
    const response = await api.get(`/options/`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    Object.assign(dbObject, response.data);
    Object.assign(localObject, response.data);
    setBreadcrumbs([]);
  } catch (error) {
    notify(`Ошибка при получении данных сервиса ${error}`, "error", false);
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
    response = await api.put("/options/", payload, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });

    Object.assign(dbObject, response.data); // Обновляем оригинальные данные
    Object.assign(localObject, response.data); // Синхронизируем локальные данные
    hasChanges.value = false; // Сбрасываем флаг изменений

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

async function loadEntity() {
  try {
    await api.post("/entity/load/", null, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });

    notify("Оборудование загружено", "success");
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
        notify("Ошибка при загрузке", "error", false);
      }
    } else {
      notify("Ошибка при загрузке", "error", false);
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

// Следим за изменениями в полях формы
watch(localObject, checkForChanges, {deep: true});

// Загрузка данных при монтировании
onMounted(() => {
  fetchData();
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