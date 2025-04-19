<script setup lang="ts">
import { useRouter, RouterLink } from 'vue-router'

const router = useRouter()


const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center space-y-6">
      <h1 class="text-6xl font-bubblegum text-amber-500">Oops! 404</h1>
      <p class="text-xl text-gray-600">
        Looks like this page has gone on a mathematical adventure!
      </p>
      <div class="space-x-4">
        <button @click="goBack"
          class="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors">
          Go Back
        </button>
        <RouterLink to="/"
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors inline-block">
          Go Home
        </RouterLink>
      </div>
    </div>
  </div>
</template>
