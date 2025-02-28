<template>
  <!--  <div class="d-flex justify-content-start m-2">-->
  <button
      class="btn btn-outline-danger me-2"
      @click="handleClick"
  >
    Удалить
  </button>
  <!--  </div>-->
</template>

<script setup>
import {defineEmits} from 'vue';

// Создаём emit-событие
const emit = defineEmits(["click-handler"]);

const handleClick = () => {
  emit("click-handler"); // Сообщаем родителю, что была нажата кнопка "Добавить"
};
</script>
