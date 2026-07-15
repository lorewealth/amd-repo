import { defineStore } from "pinia";

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
  },
})
