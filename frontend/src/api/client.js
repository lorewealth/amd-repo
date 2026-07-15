import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import router from '@/router'

const client = axios.create({
  baseURL: '/api',
})

client.interceptors.request.use((config) => {
  const token = useAuthStore().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      useAuthStore().logout()
      router.push({name:'login'})
    }
    return Promise.reject(err)
  },
)

export default client
