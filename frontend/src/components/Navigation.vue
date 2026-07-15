<script setup>

import { RouterLink, useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

function onLogout(){
  auth.logout()
  router.push({name:'runs'})
}
</script>

<template>
  <nav class="nav-wrapper">
    <template v-if="route.name === 'runs'">
      <RouterLink :to="{name: 'about'}" class="btn">Despre</RouterLink>
      <RouterLink :to="{name: 'upload'}" class="btn">Incarca</RouterLink>
    </template>
    <RouterLink v-else :to="{name:'runs'}" class="btn">Inapoi la rulari</RouterLink>
    <div v-if="auth.isAuthenticated">
      <span>{{auth.user?.email}}</span>
      <button class="btn" @click="onLogout">Logout</button>
    </div>
    <RouterLink v-else-if="route.name !== 'login'" :to="{name: 'login'}" class="btn">Login</RouterLink>
  </nav>
</template>

<style scoped>
  .nav-wrapper{
    display:flex;
    flex-direction:row;
    justify-content:center;
    align-items:center;
  }

</style>
