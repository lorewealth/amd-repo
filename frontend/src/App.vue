<script setup>
import { RouterView } from 'vue-router'
import Navigation from '@/components/Navigation.vue';

</script>

<template>
  <header>
    <div class="div-wrapper">
      <h1>Functional Coverage Dashboard</h1>
      <Navigation/>
    </div>
  </header>
  <main>
    <RouterView/>
  </main>
</template>

<style scoped>
.div-wrapper{
  display:flex;
  flex-direction:column;
  align-items:center;
  margin-top: 25px;
}
</style>
