import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: {name: 'runs'}
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/About.vue'),
    },
    {
      path: '/runs',
      name: 'runs',
      component: () => import ('@/views/RunsList.vue')
    },
    {
      path: '/runs/:id',
      name: 'runs-detail',
      component: () => import('@/views/RunDetail.vue')
    },
  ],
})

export default router
