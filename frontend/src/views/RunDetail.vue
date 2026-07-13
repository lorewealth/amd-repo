<script setup>
import { useRoute } from 'vue-router';
const route = useRoute()
</script>

<template>
  <p>Detalii pentru rularea #{{route.params.id}}</p>
</template>
