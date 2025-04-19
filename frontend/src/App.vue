<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { getSessionCookie, getFireBaseCookie } from '@/lib/helpers'


// check authentication
import { useAuthStore } from "@/stores/Authentication/authStore"

const { init } = useAuthStore()


onMounted(async () => {
  const sessionCookie = getSessionCookie()
  if (sessionCookie) {
    // Cookie exists, initialize auth state
    const firebaseCookie = getFireBaseCookie()
    if (firebaseCookie) {
      await init(sessionCookie, firebaseCookie)
      return
    }
    await init(sessionCookie, null)
  } else {
    console.log('No session cookie found')
  }
})





</script>

<template>
  <RouterView />
</template>
