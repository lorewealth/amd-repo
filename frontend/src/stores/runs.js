import { defineStore } from "pinia";
import { getRuns } from '@/api/runs'

export const useRunsStore = defineStore('runs', {
  state: () => ({
    runs: [],
    loading: false,
    error: null,
  }),
  getters: {
    sortedRuns: (state) =>
      [...state.runs].sort((a, b) => new Date(b.run_date) - new Date(a.run_date)
      ),
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
  },
})
