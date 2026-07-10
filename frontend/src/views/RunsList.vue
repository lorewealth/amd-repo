<script setup>
import {ref, onMounted} from 'vue'
import {getRuns} from '../api/runs'

const runs = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () =>{
  try{
    const res = await getRuns()
    runs.value = res.data
  }
  catch(e){
    error.value = 'Nu am putut incarca rularile'
  }
  finally{
    loading.value = false
  }
})
</script>

<template>
  <p v-if="loading">Loading...</p>
  <p v-else-if="error">{{error}}</p>
  <ul v-else>
    <p>Fisierele incarcate in db:</p>
    <li v-for="r in runs" :key="r.id">{{r.filename}} - {{r.overall_coverage}}%</li>
  </ul>
</template>
