<template>
  <nav class="nav flex-column bg-dark text-white vh-100 p-3">
    <RouterLink :to="{ name: 'home' }"
                class="mb-3">
     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1620.47 156.49" class="mt-2">
            <path class="a"
                  d="M647.86,168.21H605.81L532.73,55.55,532.31,34l-9.56,15.41-77,118.75H408.58L307.1,11.79H350l77.19,119,77.19-119h42.86l77.19,119,82.11-119h42.86L647.86,168.21ZM148.51,11.79H111.39L9.91,168.21H52.76l55.86-86.14,29.55-48.59.38,29,68.59,105.76H250L148.51,11.79Zm798.07,0H909.45L808,168.21h42.86l55.86-86.14,29.55-48.59.38,29,68.59,105.76h42.86L946.58,11.79Zm582.31,0h-37.12L1390.29,168.21h42.86L1489,82.07l29.55-48.59.38,29,68.59,105.76h42.85L1528.89,11.79ZM1123.6,150.9v17.31l127.49.05c1,.06,2.2-.08,3.44-.06s2.39-.16,3.59-.19a74.8,74.8,0,0,0,23.34-4.28,57.06,57.06,0,0,0,18.91-11,50.79,50.79,0,0,0,12.2-16,51.4,51.4,0,0,0,5-19.33h.13V80.74a75.66,75.66,0,0,0-4.86-26.85,66.36,66.36,0,0,0-13.91-22.23,61.71,61.71,0,0,0-21.32-14.58,68.38,68.38,0,0,0-26.19-4.94l-127.81-.08V150.9Zm37-89.13V60.16l-18.48-13.6c32.17,0,77.11,0,109.28,0a35,35,0,0,1,12.86,2.26,27.07,27.07,0,0,1,9.76,6.51,31.87,31.87,0,0,1,6.78,11.12,41.5,41.5,0,0,1,2.44,14.27v33.07l.07.33c0,.45-.08,1-.05,1.43a16.86,16.86,0,0,1-1.63,6.24,16.43,16.43,0,0,1-4,5.24,23.43,23.43,0,0,1-8.33,4.57,41.24,41.24,0,0,1-11.86,1.86h-2.25c-30.39-1.2-63.86.5-94.58.8V61.77Z"
                  transform="translate(-9.91 -11.79)"/>
        </svg>
      <!--    <span class="fs-4">AWADA</span>-->
    </RouterLink>
    <hr>
    <RouterLink :to="{ name: 'settings' }" :active-class="'active'" class="nav-link text-white">Настройки</RouterLink>
    <RouterLink :to="{ name: 'projects' }" :active-class="'active'" class="nav-link text-white">Проекты</RouterLink>
    <!--    <RouterLink to="/system-users" class="nav-link text-white">Системные пользователи</RouterLink>-->
    <!--    <RouterLink to="/permissions-check" class="nav-link text-white">Проверка прав</RouterLink>-->
  </nav>
</template>

<script setup>
</script>

<style scoped>
.nav-link {
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #495057;
  text-decoration: none;
}

.nav-link.active {
  background-color: #007bff;
  color: white !important;
}
</style>
