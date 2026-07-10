<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>
<template>
  <button @click="count++" type="button">Incrementeaza-ma! Currently: {{count}}</button>
</template>
