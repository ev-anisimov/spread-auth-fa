<template>
  <div class="permission-item" :class="{ 'new': props.perm.tempId, 'changed': hasChanges}">
    <select v-model="localPermission.locationId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="loc in locationList" :key="loc.obj_id" :value="loc.obj_id">
        {{ loc.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.subsystemId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="sub in typeSubgineryList" :key="sub.obj_id" :value="sub.obj_id">
        {{ sub.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.objectTypeId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="type in typeEngineryList" :key="type.obj_id" :value="type.obj_id">
        {{ type.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.engineerObjectId" class="form-control" @change="updateCode" :disabled="!isEditing">
      <option v-for="eng in engineryList" :key="eng.obj_id" :value="eng.obj_id">
        {{ eng.obj_name }}
      </option>
    </select>

    <select v-model="localPermission.access" class="form-control" @change="emitUpdate()" :disabled="!isEditing">
      <option v-for="option in accessOptions" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>

    <div class="actions">
      <!--      <button class="btn btn-danger btn-sm" @click="removePermission" :disabled="!isEditing">🗑</button>-->
      <button class="btn border-dis" role="button" @click="removePermission" :disabled="!isEditing">
        <svg width="24px" height="24px" viewBox="-3 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns"
             fill="#000000">
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <defs></defs>
            <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
              <g id="Icon-Set" sketch:type="MSLayerGroup" transform="translate(-259.000000, -203.000000)"
                 fill="#000000">
                <path
                    d="M282,211 L262,211 C261.448,211 261,210.553 261,210 C261,209.448 261.448,209 262,209 L282,209 C282.552,209 283,209.448 283,210 C283,210.553 282.552,211 282,211 L282,211 Z M281,231 C281,232.104 280.104,233 279,233 L265,233 C263.896,233 263,232.104 263,231 L263,213 L281,213 L281,231 L281,231 Z M269,206 C269,205.447 269.448,205 270,205 L274,205 C274.552,205 275,205.447 275,206 L275,207 L269,207 L269,206 L269,206 Z M283,207 L277,207 L277,205 C277,203.896 276.104,203 275,203 L269,203 C267.896,203 267,203.896 267,205 L267,207 L261,207 C259.896,207 259,207.896 259,209 L259,211 C259,212.104 259.896,213 261,213 L261,231 C261,233.209 262.791,235 265,235 L279,235 C281.209,235 283,233.209 283,231 L283,213 C284.104,213 285,212.104 285,211 L285,209 C285,207.896 284.104,207 283,207 L283,207 Z M272,231 C272.552,231 273,230.553 273,230 L273,218 C273,217.448 272.552,217 272,217 C271.448,217 271,217.448 271,218 L271,230 C271,230.553 271.448,231 272,231 L272,231 Z M267,231 C267.552,231 268,230.553 268,230 L268,218 C268,217.448 267.552,217 267,217 C266.448,217 266,217.448 266,218 L266,230 C266,230.553 266.448,231 267,231 L267,231 Z M277,231 C277.552,231 278,230.553 278,230 L278,218 C278,217.448 277.552,217 277,217 C276.448,217 276,217.448 276,218 L276,230 C276,230.553 276.448,231 277,231 L277,231 Z"
                    id="trash" sketch:type="MSShapeGroup"></path>
              </g>
            </g>
          </g>
        </svg>
      </button>
      <button class="btn border-dis" role="button" @click="clonePermission" :disabled="!isEditing">
        <svg width="24px" height="24px" viewBox="-2.4 -2.4 28.80 28.80" fill="none" xmlns="http://www.w3.org/2000/svg"
             transform="rotate(0)matrix(-1, 0, 0, -1, 0, 0)">
          <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
          <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
          <g id="SVGRepo_iconCarrier">
            <path
                d="M8 8H7.2C6.0799 8 5.51984 8 5.09202 8.21799C4.71569 8.40973 4.40973 8.71569 4.21799 9.09202C4 9.51984 4 10.0799 4 11.2V16.8C4 17.9201 4 18.4802 4.21799 18.908C4.40973 19.2843 4.71569 19.5903 5.09202 19.782C5.51984 20 6.0799 20 7.2 20H12.8C13.9201 20 14.4802 20 14.908 19.782C15.2843 19.5903 15.5903 19.2843 15.782 18.908C16 18.4802 16 17.9201 16 16.8V16M11.2 16H16.8C17.9201 16 18.4802 16 18.908 15.782C19.2843 15.5903 19.5903 15.2843 19.782 14.908C20 14.4802 20 13.9201 20 12.8V7.2C20 6.0799 20 5.51984 19.782 5.09202C19.5903 4.71569 19.2843 4.40973 18.908 4.21799C18.4802 4 17.9201 4 16.8 4H11.2C10.0799 4 9.51984 4 9.09202 4.21799C8.71569 4.40973 8.40973 4.71569 8.21799 5.09202C8 5.51984 8 6.07989 8 7.2V12.8C8 13.9201 8 14.4802 8.21799 14.908C8.40973 15.2843 8.71569 15.5903 9.09202 15.782C9.51984 16 10.0799 16 11.2 16Z"
                stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
          </g>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, defineProps, defineEmits, computed} from "vue";

const props = defineProps({
  perm: Object,
  locationList: Array,
  typeSubgineryList: Array,
  typeEngineryList: Array,
  engineryList: Array,
  isEditing: Boolean
});

const emit = defineEmits(["edit", "remove", "clone"]);

// 🔹 Локальная копия permission
const localPermission = ref({
  projectId: null,
  locationId: null,
  subsystemId: null,
  objectTypeId: null,
  engineerObjectId: null,
  access: 0,
  hasChanges: false,
});

// 🔹 Варианты доступа
const accessOptions = [
  {value: 0, label: "Полный доступ"},
  {value: 1, label: "Просмотр"},
  {value: 2, label: "Запрещено"},
];

const hasChanges = computed(() => props.perm.hasChanges || false);
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
        hasChanges: props.perm.hasChanges ?? false,
      };
    }
  }
});

// 🔹 Собираем `code` при изменении
const updateCode = () => {
  const newCode = `${localPermission.value.projectId}/${localPermission.value.locationId}/${localPermission.value.subsystemId}/${localPermission.value.objectTypeId}/${localPermission.value.engineerObjectId}`;
  localPermission.value.projectId = props.perm.project;

  // localPermission.value.hasChanges= JSON.stringify(localPermission) !== JSON.stringify(props.perm);

  emitUpdate(newCode);
};

// 🔹 Обновляем родительский компонент
const emitUpdate = (newCode = null) => {
  emit("edit", {
    ...props.perm,
    code: newCode || props.perm.code,
    access: localPermission.value.access,
    // hasChanges: JSON.stringify(localPermission) !== JSON.stringify(props.perm),
  });
};

// 🔹 Удаление permission
const removePermission = () => {
  emit("remove", props.perm);
};

const clonePermission = () => {
  emit("clone", props.perm);
};
// 🔹 Следим за изменениями
// watch(localPermission, updateCode, { deep: true });

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

.permission-item.changed {
  background-color: rgba(255, 193, 7, 0.3); /* Светло-жёлтый цвет */
}

.permission-item.new {
  background-color: aquamarine;
}
/* Кнопки действий */
.actions {
  display: flex;
  justify-content: center;
}

.border-dis {
  border: none;
}
</style>