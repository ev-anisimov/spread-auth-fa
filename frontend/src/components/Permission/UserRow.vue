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

.user {
  text-align: left;
  color: #007bff;
  cursor: pointer;
}
</style>