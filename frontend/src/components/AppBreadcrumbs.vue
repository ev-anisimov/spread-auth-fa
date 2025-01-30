<template>
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <li
        v-for="(item, index) in items"
        :key="index"
        :class="['breadcrumb-item', { active: index === items.length - 1 }]"
        aria-current="index === items.length - 1 ? 'page' : undefined"
      >
        <router-link v-if="item.url && index !== items.length - 1" :to="item.url">
          {{ item.label }}
        </router-link>
        <span v-else>{{ item.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { defineProps } from "vue";

defineProps({
  items: {
    type: Array,
    required: true,
    default: () => [],
    validator: (value) =>
      value.every(
        (item) =>
          typeof item === "object" &&
          "label" in item &&
          (typeof item.label === "string") &&
          (!item.url || typeof item.url === "string")
      ),
  },
});
</script>

<style scoped>
.breadcrumb {
  margin: 0;
  padding: 0;
  background: none;
  list-style: none;
  display: flex;
}

.breadcrumb-item {
  margin-right: 0.5rem;
}

.breadcrumb-item:last-child {
  margin-right: 0;
}

.breadcrumb-item a {
  text-decoration: none;
  color: #007bff;
}

.breadcrumb-item a:hover {
  text-decoration: underline;
}

.breadcrumb-item.active {
  font-weight: bold;
  color: #6c757d;
}
</style>
