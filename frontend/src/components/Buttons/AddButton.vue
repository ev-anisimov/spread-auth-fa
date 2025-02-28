<template>
  <button
      class="btn btn-outline-success  me-2"
      @click="handleClick"
  >
    Добавить
  </button>
</template>

<script setup>
import {defineEmits} from 'vue';

// Создаём emit-событие
const emit = defineEmits(["add-handler"]);

const handleClick = () => {
  emit("add-handler"); // Сообщаем родителю, что была нажата кнопка "Добавить"
};
</script>
