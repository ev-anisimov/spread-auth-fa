<template>
  <div class="card">

    <ToolBar>
      <template #buttons>
        <EditButton v-if="!isEditing" @click-handler="toggleEditMode"/>
        <SaveButton v-if="isEditing" @click-handler="saveChanges" :has-changes="hasChanges"
                    :is-new="isNew"/>
        <DeleteButton @click="deleteRole"/>
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
                :disabled="!isEditing"
            />
            <small v-if="errors.name" class="error-text">{{ errors.name }}</small>

          </div>
        </div>
        <!-- Вкладки проектов -->
        <ul class="nav nav-tabs">
          <li v-for="project in projects" :key="project.project_id" class="nav-item">
            <a class="nav-link"
               :class="{ active: project.project_id !== activeProjectId }"
               href="#"
               @click="changeProject(project.project_id)">
              {{ project.name }} <span :class="{'badge bg-secondary': project.project_id !== activeProjectId,
                                                  'badge bg-info': project.project_id === activeProjectId}">{{
                project.cnt
              }}</span>
            </a>
          </li>
        </ul>

        <!-- Кнопка "Добавить" -->
        <button type="button" class="btn btn-success add-btn" @click="addPermission" :disabled="!isEditing">
          <span>+</span>
        </button>

        <!-- Заголовки таблицы -->
        <div class="permissions-header">
          <div>Локация</div>
          <div>Подсистема</div>
          <div>Тип объекта</div>
          <div>Инженерный объект</div>
          <div>Доступ</div>
          <div></div>
        </div>
        <div class="role-list">
          <PermissionItem
              v-for="perm in projectPermissions"
              :key="perm.id || perm.tempId"
              :perm="perm"
              :location-list="locationList"
              :typeSubginery-list="typeSubgineryList"
              :typeEnginery-list="typeEngineryList"
              :enginery-list="engineryList"
              :is-editing="isEditing"
              :has-changes="perm.hasChanges"
              @edit="editPermission"
              @remove="removePermission"
          />
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
import PermissionItem from "@/components/Permission/PermissionItem.vue";

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
  name: "",
  permissions: [],
});

// Локальная копия данных для редактирования
const localObject = reactive({
  id: null,
  name: "",
  permissions: [],
});

// let permissionList = reactive([]);
const errors = ref({}); // Ошибки валидации

const locationList = reactive([]);
const typeSubgineryList = reactive([]);
const typeEngineryList = reactive([]);
const engineryList = reactive([]);

const projects = reactive([]);
let activeProjectId = ref(null);

const cachedPermissions = reactive({});
const origPermissions = reactive({});
const projectPermissions = computed(() => cachedPermissions[activeProjectId.value] || []);

// Переключение проекта
const changeProject = async (projectId) => {
  if (projectId) {
    activeProjectId.value = projectId;
    await fetchPermissionsForProject(projectId);
  }
};

// Проверка изменений
const checkForChanges = () => {

  let roleChanged = JSON.stringify(dbObject) !== JSON.stringify(localObject);

  let permissionsChanged = Object.values(cachedPermissions)
      .some(permissions => permissions.some(perm => perm.hasChanges));
  hasChanges.value = roleChanged || permissionsChanged;
};

// Загрузка permissions для проекта
const fetchPermissionsForProject = async (projectId) => {
  if (!dbObject.id) return;
  if (cachedPermissions[projectId]) return; // Если кеш есть — не загружаем заново
  if (!projectId) return;

  try {
    const response = await axios.get(`/api/v1/roles/${dbObject.id}/permissions?project=${projectId}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    cachedPermissions[projectId] = response.data.map(p => ({...p})); // Кешируем
    origPermissions[projectId] = response.data.map(p => ({...p})); // Кешируем
  } catch (error) {
    notify(`Ошибка загрузки прав доступа для проекта ${projectId}: ${error}`, "error");
  }
};

// Добавление нового permission
const addPermission = () => {
  if (!cachedPermissions[activeProjectId.value]) {
    cachedPermissions[activeProjectId.value] = [];
  }

  cachedPermissions[activeProjectId.value].push({
    tempId: `new-${Date.now()}`,
    project: activeProjectId.value,
    code: `${activeProjectId.value}/null/null/null/null`,
    access: 0,
    role_id: dbObject.id,
    id: null,
    hasChanges: true,
  });

  checkForChanges();
};

// Удаление permission
const removePermission = (perm) => {
  const projectId = perm.project;
  if (cachedPermissions[projectId]) {
    cachedPermissions[projectId] = cachedPermissions[projectId].filter((p) => p.id !== perm.id);
    checkForChanges();
  }
};

// Редактирование permission
const editPermission = (updatedPerm) => {
  const projectId = updatedPerm.project;
  if (!cachedPermissions[projectId]) return;

  const index = cachedPermissions[projectId].findIndex((p) => p.id === updatedPerm.id);
  if (index !== -1) {
    const origPerm = origPermissions[projectId].find((p) => p.id === updatedPerm.id);
    const cachPerm = cachedPermissions[projectId][index];
    let hasChanges;
    if ((origPerm.code === updatedPerm.code) &&
        (origPerm.access === updatedPerm.access) &&
        (origPerm.index === updatedPerm.index)) {
      hasChanges = false;
    } else if ((cachPerm.code !== updatedPerm.code) ||
        (cachPerm.access !== updatedPerm.access) ||
        (cachPerm.index !== updatedPerm.index)) {
      hasChanges = true;
    }
    cachedPermissions[projectId][index] = {...updatedPerm, hasChanges};

    checkForChanges();
  }
};

// Загрузка роли
async function fetchRole() {
  try {
    const response = await axios.get(`/api/v1/roles/${route.params.id}/`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    Object.assign(dbObject, response.data);
    Object.assign(localObject, response.data);
    setBreadcrumbs([
      {label: "Роли", url: "/roles"},
      {label: dbObject.name, url: `/roles/${dbObject.id}`},
    ]);
    await fetchPermissionsForProject(activeProjectId.value);
  } catch (error) {
    notify(`Ошибка при получении данных роли ${error}`, "error", false);
  }
}

// Загрузка проектов
async function fetchProjects() {
  try {
    const response = await axios.get(`/api/v1/projects/with_count/`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    projects.push(...response.data);
    if (projects.length > 0) {
      await changeProject(projects[0].project_id);
    }
  } catch (error) {
    notify(`Ошибка при получении проектов ${error}`, "error", false);
  }
}

async function fetchEntities(collection, type) {
  try {
    const response = await axios.get(`/api/entity/${type}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    collection.push({
		"obj_name": "*",
		"obj_type": type,
		"id": '*',
		"parent_id": null,
		"obj_id": "*",
		"updated_at": "2025-02-27T13:25:50.575900"})
    collection.push(...response.data);
  } catch (error) {
    notify(`Ошибка при получении ${error}`, "error", false);
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
    const allPermissions = [];
    for (const projectId in cachedPermissions) {
      allPermissions.push(...cachedPermissions[projectId].find(p => p.hasChanges === true));
    }
    const payload = {
      role: {...localObject},
      permissions: allPermissions
    };

    // if (isNew.value) {
    //   response = await axios.post("/api/v1/roles", payload, {
    //     headers: {Authorization: `Bearer ${authStore.token}`}
    //   });
    // } else {
    //   response = await axios.put(`/api/v1/roles/${dbObject.id}`, payload, {
    //     headers: {Authorization: `Bearer ${authStore.token}`}
    //   });
    // }
    if (isNew.value) {
      response = await axios.post("/api/v1/roles", payload, {
        headers: {Authorization: `Bearer ${authStore.token}`}
      });
    } else {
      response = await axios.put(`/api/v1/roles/${dbObject.id}/permissions`, payload, {
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
        notify("Ошибка при сохранении роли", "error", false);
      }
    } else {
      notify("Ошибка при сохранении роли", "error", false);
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
async function deleteRole() {
  if (!confirm("Вы уверены, что хотите удалить роль?")) return;
  try {
    await axios.delete(`/api/v1/roles/${dbObject.id}`, {
      headers: {Authorization: `Bearer ${authStore.token}`}
    });
    await router.push("/roles"); // Редирект на список пользователей
  } catch (error) {
    notify(`Ошибка при удалении пользователя ${error}`, "error", false);
  }
}

// Следим за изменениями в полях формы
watch(localObject, checkForChanges, {deep: true});

// Загрузка данных при монтировании
onMounted(() => {
  if (!isNew.value) {
    fetchRole();
  }
  fetchProjects();
  fetchEntities(locationList, 'locations')
  fetchEntities(typeSubgineryList, 'type_subginery')
  fetchEntities(typeEngineryList, 'type_enginery')
  fetchEntities(engineryList, 'enginery')
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

.permissions-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 100px;
  font-weight: bold;
  background-color: #f8f9fa;
  padding: 10px;
  border-bottom: 1px solid #dee2e6;
}

.add-btn {
  top: -10px;
  left: -10px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>