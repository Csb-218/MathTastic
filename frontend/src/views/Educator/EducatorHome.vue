<script setup lang="ts">
import NavbarEducator from '@/components/blocks/navigation/NavbarEducator.vue'
import { RouterView } from 'vue-router'



</script>

<template>
  <div class="min-h-screen bg-gradient-to-b py-10 from-amber-50 to-white">
    <NavbarEducator />
    <RouterView />
  </div>
</template>
