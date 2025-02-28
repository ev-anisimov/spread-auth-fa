<template>
  <button
      class="btn btn-outline-success me-2"
      @click="handleClick"
      :disabled="!hasChanges"
  >
    {{ isNew ? "Создать" : "Сохранить изменения" }}
  </button>
</template>

<script setup>
import {defineEmits, defineProps} from 'vue';

defineProps({
  isNew: {
    type: Boolean,
    required: true
  },
  hasChanges: {
    type: Boolean,
    required: true
  }
});

// Создаём emit-событие
const emit = defineEmits(["click-handler"]);

const handleClick = () => {
  emit("click-handler"); // Сообщаем родителю, что была нажата кнопка "Добавить"
};
</script>
