<script setup>

import { RouterLink, useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

function onLogout(){
  auth.logout()
  router.push({name:'login'})
}
</script>

<template>

  <nav class="nav-wrapper">
    <div class="nav-left">
      <h1>Functional Coverage Dashboard</h1>
      <template v-if="route.name === 'runs'">
        <RouterLink :to="{name: 'about'}" class="btn">Despre</RouterLink>
        <RouterLink v-if="auth.isAuthenticated" :to="{name: 'upload'}" class="btn">Incarca</RouterLink>
      </template>
      <RouterLink v-else-if="route.name !== 'login'" :to="{name:'runs'}" class="btn">Inapoi la rulari</RouterLink>
    </div>
    <div v-if="auth.isAuthenticated" class="nav-right">
      <span>{{auth.user?.email}}</span>
      <button class="btn" @click="onLogout">Logout</button>
    </div>
    <RouterLink v-else-if="route.name !== 'login'" :to="{name: 'login'}" class="btn">Login</RouterLink>
  </nav>
</template>

<style scoped>
  .nav-wrapper{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
  }
  .nav-left, .nav-right{
    display:flex;
    align-items:center;
    gap:8px;
  }
  h1{
    font-size:1.4rem;
  }

</style>
