<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navigation from '@/components/Navigation.vue'

</script>

<template>
  <header>
    <div class="nav-wrapper">
      <h1>Functional Coverage Dashboard</h1>
      <Navigation/>
    </div>
  </header>
  <main class="content">
    <RouterView/>
  </main>
</template>

<style scoped>
.nav-wrapper{
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
}
.content{
  display:flex;
  justify-content:center;
}
</style>
