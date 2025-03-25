<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { getSessionCookie } from '@/lib/helpers'


// check authentication
import { useAuthStore } from "@/stores/authentication"

const { init } = useAuthStore()


onMounted(async () => {
  const sessionCookie = getSessionCookie()
  if (sessionCookie) {
    // Cookie exists, initialize auth state
    await init(sessionCookie)
  } else {
    console.log('No session cookie found')
  }
})





</script>

<template>
  <RouterView />
</template>
