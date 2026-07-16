import { defineStore } from "pinia";
import { getRun, getRuns } from '@/api/runs'

export const useRunsStore = defineStore('runs', {
  state: () => ({
    runs: [],
    loading: false,
    error: null,
    current: null,
    currentLoading: false,
    currentError: null,
  }),
  getters: {
    totalRuns: (state) => state.runs.length,
    avgCoverage: (state) =>
      state.runs.length ? state.runs.reduce((s, r) => s + Number(r.overall_coverage), 0) / state.runs.length : 0,
  },
  actions: {
    async fetchRuns() {
      this.loading = true
      this.error = null
      try {
        const { data } = await getRuns()
        this.runs = data
      }
      catch (e) {
        this.error = 'Nu am putut incarca rularile'
      }
      finally {
        this.loading = false
      }
    },
    async fetchRun(id) {
      this.currentLoading = true
      this.current = null
      this.currentError = null
      try {
        const { data } = await getRun(id)
        this.current = data
      }
      catch (e) {
        this.currentError = e.response?.status ?? 'network'
      }
      finally {
        this.currentLoading = false
      }
    },
  },
})
