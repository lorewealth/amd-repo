import axios from 'axios'

export const API_BASE = '/api'

const client = axios.create({
  baseURL: API_BASE,
})

let getToken = () => null
let handleUnauth = () => { }

export function setupAuthHooks(hooks) {
  getToken = hooks.getToken
  handleUnauth = hooks.handleUnauth
}

client.interceptors.request.use((config) => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      handleUnauth()
    }
    return Promise.reject(err)
  },
)

export default client
