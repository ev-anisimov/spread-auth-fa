<template>
  <button
      class="btn btn-outline-success me-2"
      @click="handleClick"
  >
    Редактировать
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
