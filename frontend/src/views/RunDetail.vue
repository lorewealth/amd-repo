<script setup>
import { useRoute } from 'vue-router';
const route = useRoute()
import BinCell from '@/components/BinCell.vue';
import CoverageBar from '@/components/CoverageBar.vue';
import { onMounted } from 'vue';
import { covBadgeClass, covStatus, fmtDate, fmtPercent } from '@/utils/format';
import { storeToRefs } from 'pinia';
import { useRunsStore } from '@/stores/runs';

const store = useRunsStore()
const { current: run, currentLoading: loading, currentError: error } = storeToRefs(store)

onMounted(async () => store.fetchRun(route.params.id))

</script>

<template>
  <p v-if="loading">Loading...</p>
  <div v-else-if="error === 404">
    <p>Rularea #{{route.params.id}} nu exista</p>
  </div>
  <p v-else-if="error">Nu am putut incarca datele</p>
  <div class="displaying" v-else-if="run">
    <div class="card">
      <p>Detalii pentru rularea #{{route.params.id}}:</p>
      <p>Fisier: {{run.filename}}</p>
      <p>Data rularii: {{fmtDate(run.run_date)}}</p>
      <p v-if="run.uploaded_by">Urcat de: {{run.uploaded_by}}</p>
      <p>Procentaj general: {{fmtPercent(run.overall_coverage)}}%</p>
      <p>
        Rezultat: <span class="badge" :class="covBadgeClass(run.overall_coverage)">{{ covStatus(run.overall_coverage) }}</span>
      </p>
      <p>Binuri ratate: {{run.missed_bins}}/{{run.total_bins}}</p>
      <CoverageBar label="OVERALL" :percent="run.overall_coverage"/>
      <div class="legend">
        <span :style="{opacity: 0.7}">Legenda culorii:</span>
        <span class="swatch c-green"></span> HIT - bin atins
        <span class="swatch c-red"></span> MISS - bin neatins
      </div>
    </div>
    <div class="cp-card" v-for="cp in run.coverpoints" :key="cp.name">
      <CoverageBar :label="cp.name" :percent="cp.coverage"/>
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
.cp-card{
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
}
.card{
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
}
.displaying{
  display:flex;
  flex-direction:column;
  gap:24px;
  max-width:min(1300px, 95%);
  margin: 0 auto;
  margin-bottom: 25px;
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
.cp-summary{
  display:block;
  margin-bottom:14px;
  font-size:0.85rem;
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
