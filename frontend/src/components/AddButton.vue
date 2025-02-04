<template>
  <div class="d-flex justify-content-start mb-4">
    <button type="button" class="btn btn-success" @click="handleClick">Добавить</button>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

// Создаём emit-событие
const emit = defineEmits(["add-handler"]);

const handleClick = () => {
  emit("add-handler"); // Сообщаем родителю, что была нажата кнопка "Добавить"
};
</script>
