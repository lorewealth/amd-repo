import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { setupAuthHooks } from '@/api/client'

import App from './App.vue'
import router from '@/router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
const auth = useAuthStore()
auth.loadFromStorage()

setupAuthHooks({
  getToken: () => auth.token,
    handleUnauth: () => {
      auth.logout()
      router.push({ name: 'login'})
    },
})
app.use(router)

app.mount('#app')
