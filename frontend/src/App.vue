<script setup>
import { RouterView } from 'vue-router'
import Navigation from '@/components/Navigation.vue';

</script>

<template>
  <header>
    <div class="div-wrapper">
      <Navigation/>
    </div>
  </header>
  <main>
    <RouterView/>
  </main>
</template>

<style scoped>
.div-wrapper{
  padding: 16px 24px;
}
</style>
