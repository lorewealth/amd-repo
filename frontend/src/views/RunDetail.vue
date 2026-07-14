<script setup>
import { useRoute } from 'vue-router';
const route = useRoute()
import BinCell from '@/components/BinCell.vue';
import CoverageBar from '@/components/CoverageBar.vue';
import { getRun } from '@/api/runs';
import { onMounted, ref } from 'vue';
import { fmtDate } from '@/utils/format';


const run = ref(null)
const loading = ref(true)
const error = ref(null)

onMounted(async () =>{
  try{
    const response = await getRun(route.params.id)
    run.value = response.data
  }
  catch(e){
    error.value = e.response?.status ?? 'network'
  }
  finally{
    loading.value = false
  }
})

</script>

<template>
  <p v-if="loading">Loading...</p>
  <div v-else-if="error === 404">
    <p>Rularea #{{route.params.id}} nu exista</p>
    <RouterLink :to="{name:'runs'}" class="btn">Inapoi la rulari</RouterLink>
  </div>
  <p v-else-if="error">Nu am putut incarca datele</p>
  <div class="displaying" v-else="run">
    <RouterLink :to="{name:'runs'}" class="btn">Inapoi la rulari</RouterLink>
    <div>
      <p>Detalii pentru rularea #{{route.params.id}}:</p>
      <p>Fisier: {{run.filename}}</p>
      <p>Data rularii: {{fmtDate(run.run_date)}}</p>
      <p>Procentaj general: {{run.overall_coverage}}%</p>
      <p>Rezultat: {{run.result}}</p>
      <p>Binuri ratate: {{run.missed_bins}}/{{run.total_bins}}</p>
      <CoverageBar class="cp-bar" label="OVERALL" :percent="run.overall_coverage"/>
      <div class="legend">
        <span :style="{opacity: 0.7}">Legenda culorii:</span>
        <span class="swatch c-green"></span> HIT - bin atins
        <span class="swatch c-red"></span> MISS - bin neatins
      </div>
    </div>
    <div v-for="cp in run.coverpoints" :key="cp.name">
      <CoverageBar class="cp-bar" :label="cp.name" :percent="cp.coverage"/>
      <span class="cp-summary">
        {{cp.total_bins - cp.missed_bins}}/{{cp.total_bins}} bin-uri atinse
      </span>
      <div class="bin-grid" :class="cp.name === 'cp_vec' ? 'grid-4x4' : 'grid-rows'">
        <BinCell v-for="b in cp.bins" :key="b.name" :bin="b"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cp-bar{
  margin: 5px 0 4px 0;
}
.displaying{
  display:flex;
  flex-direction:column;
  gap:24px;
  max-width:750px;
  margin: 0 auto;
}
.bin-grid{
  display:grid;
  gap:8px;
}
.grid-4x4{
  grid-template-columns: repeat(4, 1fr);
}
.grid-rows{
  grid-template-columns: 1fr;
}
.legend{
  display:flex;
  align-items: center;
  gap:6px;
  font-size:0.85rem;
}
.cp-summary{
  display:block;
  margin-bottom:14px;
  font-size:0.85rem;
}
.swatch{
  width:12px;
  height:12px;
  border-radius:3px;
  display:inline-block;
}
.c-green{
  background: rgba(63, 185, 80, 1);
}
.c-red{
  background: rgba(248, 81, 73, 1.0);
}
.btn{
  font-size: 0.85rem;
  opacity: 0.7;
  text-decoration: none;
  color: inherit;
  align-self: center;
}
.btn:hover{
  opacity: 1;
}

</style>
