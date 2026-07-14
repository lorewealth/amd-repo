<script setup>

import { RouterLink } from 'vue-router';

</script>

<template>
  <nav>
    <RouterLink :to="{name: 'runs'}" class="btn">Rulari</RouterLink>
    <RouterLink :to="{name: 'about'}" class="btn">Despre</RouterLink>
  </nav>
</template>

<style scoped>
  .btn{
    display: inline-block;
    padding: 0.5em 1em;
    background-color: #3a3a3a;
    color: white;
    border-radius: 4px;
    text-decoration: none;
    margin: 5px;
  }
  .btn:hover{
    background-color: #4a4a4a;
  }
  .btn.router-link-active{
    background-color: #d3d8d3
  }
</style>
