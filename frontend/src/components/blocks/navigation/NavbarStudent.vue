<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="bg-white shadow-md fixed w-full top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex-shrink-0 flex items-center">
          <h1 class="text-2xl sm:text-3xl font-bold text-amber-500">MathTastic</h1>
        </div>
        <div class="hidden sm:flex items-center gap-x-4">
          <button @click="handleLogout" class="text-gray-700 hover:text-blue-600 transition-colors">
            Logout
          </button>
        </div>
        <!-- Mobile menu button -->
        <div class="flex items-center sm:hidden">
          <button class="text-gray-500 hover:text-gray-700">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
