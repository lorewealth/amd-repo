<script setup>
import { ref, computed, onMounted } from 'vue'
import { covBadgeClass, covClass, covStatus, fmtDate, fmtPercent } from '@/utils/format'
import { useRouter } from 'vue-router'
import { useRunsStore } from '@/stores/runs'
import CoverageBar from '@/components/CoverageBar.vue'
const store = useRunsStore()
const sortKey = ref('run_date')
const sortDir = ref('desc')
const router = useRouter()

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
    if(sortKey.value === 'overall_coverage' || sortKey.value === 'result'){
      valA = Number(a.overall_coverage)
      valB = Number(b.overall_coverage)
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
  {key:'result', label:'Rezultat'},
]

onMounted(async () =>{
  store.fetchRuns()
})

</script>

<template>
  <p v-if="store.loading">Loading...</p>
  <p v-else-if="store.error">{{store.error}}</p>
  <div class="content" v-else>
    <p v-if="store.totalRuns === 0" class="empty">Nicio rulare inca - urca una</p>
    <div v-else>
      <p>Nr. de rulari: {{store.totalRuns}}</p>
      <CoverageBar label="Average-ul" :percent="fmtPercent(store.avgCoverage)"/>
      <div class="legend">
        <span :style="{opacity: 0.7}">Legenda culorii:</span>
        <span class="swatch c-green"></span> PASSED
        <span class="swatch c-yellow"></span> FAILED dar admisibil
        <span class="swatch c-red"></span> FAILED
      </div>
      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th v-for="col in cols" :key="col.key" @click="sortBy(col.key)">
                {{col.label}} <span v-if="sortKey === col.key">{{ sortDir === 'asc' ? '▲' : '▼'}}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="run in dispRuns" :key="run.id" tabindex="0" @click="router.push(`/runs/${run.id}`)" @keydown.enter="router.push(`/runs/${run.id}`)">
              <td>{{ fmtDate(run.run_date) }}</td>
              <td>{{ run.filename }}</td>
              <td :class="covClass(run.overall_coverage)">
                {{ fmtPercent(run.overall_coverage) }}%
              </td>
              <td>
                <span class="badge" :class="covBadgeClass(run.overall_coverage)">
                  {{ covStatus(run.overall_coverage) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .empty{
    text-align: center;
      margin-top: 60px;
      font-size: 1.1rem;
      opacity: 0.8;
  }
  .content{
    max-width:min(1300px, 95%);
    margin: 0 auto;
  }
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
  .badge-good{
    color: #3fb950;
    background: rgba(46, 160, 67, 0.15);
  }
  .badge-warn{
    color: #d29922;
    background: rgba(210, 153, 34, 0.15);
  }
  .badge-bad{
    color: #f85149;
    background: rgba(248, 81, 73, 0.15);
  }
  .table-wrap{
    margin: 15px 0px 20px 0px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    overflow: auto;
    height:250px;
  }
  .table{
    border-collapse: separate;
    border-spacing:0;
    width: 100%;
    table-layout:auto;
  }
  .table td, .table th {
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 10px 25px;
    text-align:center;
  }
  .table th{
    position:sticky;
    background: rgba(0, 51, 79, 1.0);
    top: 0;
    z-index: 2;
  }
  tbody tr:hover{
    background-color:#3a3a3a;
    cursor:pointer;
  }
</style>
