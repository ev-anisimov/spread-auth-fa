<template>
  <button
      :class="['btn','me-2', btnCls]"
      @click="handleClick"
      :disabled="!hasChanges"
  >
    {{ title }}
  </button>
</template>

<script setup>
import {defineEmits, defineProps} from 'vue';

defineProps({
  title: {
    type: String,
    required: true
  },
  btnCls: {
    type: String,
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
