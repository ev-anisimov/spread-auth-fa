<template>
  <div class="role-row" @click="openCard">
    <div class="role">{{ props.name }}</div>
    <div> <span class="badge bg-info">{{props.cnt }}</span></div>
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
  },
  cnt:{
    type:Number,
    required:false,
  }
});
const router = useRouter();

function openCard() {
  router.push({name: 'rolecard', params: {id: props.id}});
}
</script>

<style scoped>


/* Строка пользователя */
.role-row {
  display: grid;
  grid-template-columns: 2fr 1fr; /* Соответствует заголовкам */
  padding: 10px 0 10px 5px;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.role-row:hover {
  background-color: #f1f3f5;
}

.role {
  text-align: left;
  color: #007bff;
  cursor: pointer;
}
</style>