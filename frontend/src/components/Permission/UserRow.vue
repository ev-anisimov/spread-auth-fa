<template>
  <div class="user-row" @click="openCard">
    <div class="user">{{ props.fullName }}</div>
    <div class="user">{{ props.username }}</div>
  </div>
</template>

<script setup>
import {defineProps} from 'vue';
import {useRouter} from "vue-router";

const props = defineProps({
  id: {
    type: [String, Number],
    required: false
  },
  fullName: {
    type: String,
    required: true
  },
  username: {
    type: String,
    required: true
  }
});
const router = useRouter();

function openCard() {
  router.push({name: 'usercard', params: {id: props.id}});
}
</script>

<style scoped>

/* Строка пользователя */
.user-row {
  display: grid;
  grid-template-columns: 2fr 1fr; /* Соответствует заголовкам */
  padding: 10px 0 10px 5px;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.user-row:hover {
  background-color: #f1f3f5;
}

.user {
  text-align: left;
  color: #007bff;
  cursor: pointer;
}
</style>