<template>
  <div class="permission-item">
    <select v-model="localPermission.locationId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="loc in locations" :key="loc.obj_id" :value="loc.obj_id">
        {{ loc.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.subsystemId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="sub in typeSubginery" :key="sub.obj_id" :value="sub.obj_id">
        {{ sub.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.objectTypeId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="type in typeEnginery" :key="type.obj_id" :value="type.obj_id">
        {{ type.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.engineerObjectId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="eng in engineries" :key="eng.obj_id" :value="eng.obj_id">
        {{ eng.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.access" class="form-control" @change="emitUpdate" :disabled="!isEditing">
      <option v-for="option in accessOptions" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>

    <div class="actions">
<!--      <button class="btn btn-danger btn-sm" @click="removePermission" :disabled="!isEditing">🗑</button>-->
      <button class="btn border-dis" role="button" @click="removePermission" :disabled="!isEditing">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash"
                 viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
            </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, defineProps, defineEmits } from "vue";

const props = defineProps({
  perm: Object,
  locations: Array,
  typeSubginery: Array,
  typeEnginery: Array,
  engineries: Array,
  isEditing: Boolean,
});

const emit = defineEmits(["edit", "remove"]);

// 🔹 Локальная копия permission
const localPermission = ref({
  projectId: null,
  locationId: null,
  subsystemId: null,
  objectTypeId: null,
  engineerObjectId: null,
  access: 0,
});

// 🔹 Варианты доступа
const accessOptions = [
  { value: 0, label: "Полный доступ" },
  { value: 1, label: "Просмотр" },
  { value: 2, label: "Запрещено" },
];

// 🔹 Разбираем `code` при инициализации
onMounted(() => {
  if (props.perm) {
    const parts = props.perm.code.split("/");
    if (parts.length === 5) {
      localPermission.value = {
        projectId: props.perm.project,
        locationId: parts[1] || null,
        subsystemId: parts[2] || null,
        objectTypeId: parts[3] || null,
        engineerObjectId: parts[4] || null,
        access: props.perm.access ?? 0,
      };
    }
  }
});

// 🔹 Собираем `code` при изменении
const updateCode = () => {
  localPermission.value.projectId = props.perm.project;
  const newCode = `${localPermission.value.projectId}/${localPermission.value.locationId}/${localPermission.value.subsystemId}/${localPermission.value.objectTypeId}/${localPermission.value.engineerObjectId}`;

  emitUpdate(newCode);
};

// 🔹 Обновляем родительский компонент
const emitUpdate = (newCode = null) => {
  emit("edit", { ...props.perm, code: newCode || props.perm.code, access: localPermission.value.access });
};

// 🔹 Удаление permission
const removePermission = () => {
  emit("remove", props.perm);
};

// 🔹 Следим за изменениями
watch(localPermission, updateCode, { deep: true });

</script>

<style scoped>
/* Основной контейнер */
.permission-item {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 100px;
  gap: 10px;
  padding: 10px;
  border-bottom: 1px solid #dee2e6;
  align-items: center;
}

/* Кнопки действий */
.actions {
  display: flex;
  justify-content: center;
}
.border-dis{
  border: none;
}
</style>