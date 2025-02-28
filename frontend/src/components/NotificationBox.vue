<template>
  <div class="notification-container">
    <transition-group name="fade">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="notification"
        :class="message.type"
        @click="removeMessage(index)"
      >
        {{ message.text }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import {ref, defineExpose} from "vue";

const messages = ref([]);

// Добавляем сообщение
const addMessage = (text, type = "success", autoClose = true) => {
  messages.value.push({text, type});

  if (autoClose) {
    setTimeout(() => {
      removeMessage(0);
    }, 3000);
  }
};

// Удаление сообщения
const removeMessage = (index) => {
  if (messages.value[index]) {
    messages.value.splice(index, 1);
  }
};

// Экспортируем метод
defineExpose({addMessage});
</script>

<style scoped>
/* Контейнер для сообщений */
.notification-container {
  position: fixed;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1000;
}

/* Стили сообщений */
.notification {
  min-width: 250px;
  max-width: 400px;
  padding: 12px 16px;
  margin-bottom: 10px;
  border-radius: 5px;
  font-size: 14px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  border: 1px solid #ccc;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Цвета сообщений */
.success {
  border-color: #28a745;
  color: #155724;
}

.error {
  border-color: #dc3545;
  color: #721c24;
}

.warning {
  border-color: blueviolet;
  color: darkviolet;
}
/* Анимация */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
