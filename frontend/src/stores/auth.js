import { defineStore } from "pinia";
import { exchangeCode } from '@/api/auth'
import { jwtPayload } from '@/utils/jwt'

export const useAuthStore = defineStore('auth', {
  state: () => ({ token: null, user: null }),
  getters: { isAuthenticated: (s) => !!s.token },
  actions: {
    setSession(token, email) {
      this.token = token
      this.user = { email }
      localStorage.setItem('fcd-token', token)
      localStorage.setItem('fcd-email', email)
    },
    loadFromStorage() {
      const email = localStorage.getItem('fcd-email')
      this.user = email ? { email } : null
      this.token = localStorage.getItem('fcd-token')
    },
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('fcd-email')
      localStorage.removeItem('fcd-token')
    },
    async handleCallback(code){
      const data = await exchangeCode(code)
      const email = jwtPayload(data.access_token).sub
      this.setSession(data.access_token, email)
    },
  },
})
