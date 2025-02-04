<template>
  <div class="notifications">
    <div
      v-for="(message, index) in messages"
      :key="index"
      :class="['notification', message.type]"
      @click="removeMessage(index)"
    >
      {{ message.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, defineExpose } from "vue";

const messages = ref([]);

const addMessage = (text, type = "success", autoClose = true) => {
  messages.value.push({ text, type });

  if (autoClose) {
    setTimeout(() => {
      messages.value.shift();
    }, 3000);
  }
};

const removeMessage = (index) => {
  messages.value.splice(index, 1);
};

defineExpose({ addMessage });
</script>

<style scoped>
.notifications {
  position: fixed;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1000;
}

.notification {
  padding: 10px 15px;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
  transition: opacity 0.3s;
}

.notification.success {
  background-color: green;
}

.notification.error {
  background-color: red;
}
</style>
