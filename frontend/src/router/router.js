import {createRouter, createWebHistory} from 'vue-router'
import permissionRoute from "@/router/permissionRoute";
import projectorRoute from "@/router/projectorRoute";
import {useAuthStore} from "@/stores/auth";

const routes = [
    ...permissionRoute,
    ...projectorRoute,
    {
        path: '/',
        name: 'home',
        component: () => import(/* webpackChunkName: "about" */ '../App.vue')
    },
      {
        path: '/login',
        name: 'login',
        component: () => import(/* webpackChunkName: "about" */ '../views/LoginView.vue')
    },
]

const mainRouter = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

mainRouter.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default mainRouter
