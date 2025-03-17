<script setup lang="ts">
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'


// check authentication
import { useAuthStore } from "@/stores/authentication"

const authState = useAuthStore()


onMounted(async () => {

  const cookies = document.cookie.split(';')
  const sessionCookie = cookies.find(cookie => cookie.trim().startsWith('user'))

  if (sessionCookie) {
    // Cookie exists, initialize auth state
    await authState.init(sessionCookie)
  } else {
    console.log('No session cookie found')
  }
})





</script>

<template>
  <RouterView />
</template>
