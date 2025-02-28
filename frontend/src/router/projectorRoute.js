
export default [
    {
        path: '/settings/',
        name: 'settings',
        component: () => import(/* webpackChunkName: "about" */ '../views/Projector/SettingsView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/projects/',
        name: 'projects',
        component: () => import(/* webpackChunkName: "about" */ '../views/Projector/ProjectsPage.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/projects/:id',
        name: 'projectcard',
        component: () => import(/* webpackChunkName: "about" */ '../components/Projector/ProjectCard.vue'),
        meta: {requiresAuth: true}
    }
];
