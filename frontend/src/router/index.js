import { useAuthStore } from '@/stores/auth'
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
      meta: {requiresAuth: true}
    },
    {
      path: '/runs',
      name: 'runs',
      component: () => import('@/views/RunsList.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/runs/:id',
      name: 'run-detail',
      component: () => import('@/views/RunDetail.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/Upload.vue'),
      meta: {requiresAuth: true}
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue')
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return {name: 'login', query: {redirect: to.fullPath}}
  }
  return true
})

export default router
