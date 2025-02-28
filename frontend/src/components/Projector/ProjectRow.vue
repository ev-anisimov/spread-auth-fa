<template>
  <div class="row" @click="openCard">
    <div class="item">{{ props.name }}</div>
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
  name: {
    type: String,
    required: true
  }
});
const router = useRouter();

function openCard() {
  router.push({name: 'projectcard', params: {id: props.id}});
}
</script>

<style scoped>


/* Строка пользователя */
.row {
  display: grid;
  grid-template-columns: 2fr 1fr; /* Соответствует заголовкам */
  padding: 10px 0 10px 5px;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.row:hover {
  background-color: #f1f3f5;
}

.item {
  text-align: left;
  color: #007bff;
  cursor: pointer;
}
</style>