// import { createRouter, createWebHistory } from 'vue-router'
// // import HomeView from '../views/HomeView.vue'
//
// const routes = [
//
//     {
//     path: '/users/',
//     name: 'users',
//     component: () => import(/* webpackChunkName: "about" */ '../views/HomeView.vue')
//   },
//     {
//     path: '/projector/',
//     name: 'projector',
//     component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
//   }
//   // {
//   //   path: '/',
//   //   name: 'home',
//   //   component: HomeView
//   // },
//   // {
//   //   path: '/about',
//   //   name: 'about',
//   //   // route level code-splitting
//   //   // this generates a separate chunk (about.[hash].js) for this route
//   //   // which is lazy-loaded when the route is visited.
//   //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
//   // }
// ]
//
// const permissionRoutes = createRouter({
//   history: createWebHistory(process.env.BASE_URL),
//   routes
// })

export default [
    {
        path: '/users/',
        name: 'users',
        component: () => import(/* webpackChunkName: "about" */ '../views/Permission/UserPage.vue'),
        meta: {requiresAuth: true}
        // children:[
        //     {
        //         path:'qq',
        //         component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
        //     }
        // ]
    },
    {
        path: '/users/:id',
        name: 'usercard',
        component: () => import(/* webpackChunkName: "about" */ '../components/Permission/UserCard.vue'),
        meta: {requiresAuth: true}
    },
    {
        path: '/roles/',
        name: 'roles',
        component: () => import(/* webpackChunkName: "about" */ '../views/Permission/RolePage.vue'),
        meta: {requiresAuth: true}
        // children:[
        //     {
        //         path:'qq',
        //         component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
        //     }
        // ]
    },
    {
        path: '/roles/:id',
        name: 'rolecard',
        component: () => import(/* webpackChunkName: "about" */ '../components/Permission/RoleCard.vue'),
        meta: {requiresAuth: true}
    }
];
