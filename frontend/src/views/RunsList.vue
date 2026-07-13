<script setup>
import {ref, computed, onMounted} from 'vue'
import { covClass, fmtDate, fmtPct } from '@/utils/format'
import router from '@/router/index'
import { useRunsStore } from '@/stores/runs'

const store = useRunsStore()
const sortKey = ref('run_date')
const sortDir = ref('desc')

function sortBy(key) {
  if(sortKey.value === key){
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  }
  else{
    sortKey.value = key
    sortDir.value = 'asc'
  }
}

const dispRuns = computed(() => {
  return [...store.runs].sort((a, b) => {
    let valA = a[sortKey.value]
    let valB = b[sortKey.value]

    if(sortKey.value === 'run_date') {
      valA = new Date(valA);
      valB = new Date(valB)
    }
    if(sortKey.value === 'overall_coverage'){
      valA = Number(valA)
      valB = Number(valB)
    }
    if(valA < valB) return sortDir.value === 'asc' ? -1 : 1
    if(valA > valB) return sortDir.value === 'asc' ? 1 : -1
    return 0
  })
})

const cols = [
  {key:'run_date', label:'Data'},
  {key:'filename', label:'Fisier'},
  {key:'overall_coverage', label:'Acoperire'},
]

onMounted(async () =>{
  store.fetchRuns()
})

</script>

<template>
  <p v-if="store.loading">Loading...</p>
  <p v-else-if="store.error">{{store.error}}</p>
  <div v-else>
    <p v-if="store.totalRuns === 0">Nicio rulare inca - urca una</p>
    <div v-else>
      <p>Nr. de rulari: {{store.totalRuns}}</p>
      <p>Average-ul: <span :class="covClass(store.avgCoverage)">{{fmtPct(store.avgCoverage)}}</span></p>
      <table>
        <thead>
          <tr>
            <th v-for="col in cols" :key="col.key" @click="sortBy(col.key)">
              {{col.label}} <span v-if="sortKey === col.key">{{ sortDir === 'asc' ? '⌃' : '⌄'}}</span>
            </th>
            <th>Rezultat</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="run in dispRuns" :key="run.id" @click="router.push(`/runs/${run.id}`)">
            <td>{{ fmtDate(run.run_date) }}</td>
            <td>{{ run.filename }}</td>
            <td :class="covClass(run.overall_coverage)">
              {{ fmtPct(run.overall_coverage) }}
            </td>
            <td>
              <span class="badge" :class="run.result.toLowerCase()">
                {{ run.result }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
  .cov-good{
    color: #2e7d32;
  }
  .cov-warn{
    color: #f9a825;
  }
  .cov-bad{
    color: #c62828;
  }
  .badge{
    padding: 2px 8px;
    border-radius: 4px;
  }
  .badge.passed{
    color: #2e7d32;
  }
  .badge.failed{
    color: #c62828;
  }
  table{
    border-collapse: collapse;
    width: 100%;
  }
  td, th {
    border: 1px solid #FFFFFF;
    padding: 10px 25px;
    text-align:center;
  }
  tbody tr:hover{
    background-color:#3a3a3a;
    cursor:pointer;
  }
</style>
