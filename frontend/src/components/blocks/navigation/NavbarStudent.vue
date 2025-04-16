<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import calculator_logo from "@/assets/icons/calculator_logo.png"
import { X, AlignJustify } from 'lucide-vue-next';
import { RouterLink } from 'vue-router';
const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}
const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <!-- Component: Navbar -->
  <header class="bg-white shadow-md fixed w-full top-0 z-50">
    <div class="max-w-screen-2xl mx-auto px-2 sm:px-4 lg:px-6">
      <nav aria-label="main navigation" class="flex h-16 items-stretch justify-between" role="navigation">
        <!-- Brand logo -->
        <RouterLink to="/" class="flex-shrink-0 flex items-center gap-x-2">
          <img :src="calculator_logo" alt="MathTastic" class="h-8 w-8" />
          <p class="text-2xl sm:text-4xl font-bubblegum text-amber-500">MathTastic</p>
        </RouterLink>

        <!-- Desktop Navigation links -->
        <ul class="hidden sm:flex items-center gap-x-4">
          <li class="flex items-stretch">
            <RouterLink to="/student" class="text-gray-700 hover:text-blue-600 transition-colors">
              Dashboard
            </RouterLink>
          </li>
          <li class="flex items-stretch">
            <button @click="handleLogout" class="text-gray-700 hover:text-blue-600 transition-colors">
              Logout
            </button>
          </li>
        </ul>

        <!-- Mobile trigger -->
        <button class="flex items-center sm:hidden text-gray-500 hover:text-gray-700" :aria-expanded="isMobileMenuOpen"
          @click="toggleMobileMenu" aria-label="Toggle navigation">
          <X v-if="isMobileMenuOpen" class="h-6 w-6" />
          <AlignJustify v-else class="h-6 w-6" />
        </button>
      </nav>

      <!-- Mobile Menu Container -->
      <div v-if="isMobileMenuOpen" class="sm:hidden fixed inset-x-0 top-16 z-50">
        <!-- Mobile Navigation Menu -->
        <div class="bg-white shadow-lg h-[50vh] overflow-y-auto relative z-20">
          <ul class="px-2 pt-4 pb-3 space-y-2 flex flex-col">
            <li>
              <RouterLink to="/student"
                class="block px-4 py-3 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                @click="isMobileMenuOpen = false">
                Dashboard
              </RouterLink>
            </li>
            <li>
              <button @click="() => { handleLogout(); isMobileMenuOpen = false; }"
                class="w-full text-left px-4 py-3 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50">
                Logout
              </button>
            </li>
          </ul>
        </div>
        <!-- Backdrop below menu -->
        <div class="fixed inset-x-0 top-[50vh] bottom-0 bg-black bg-opacity-25 z-10" @click="isMobileMenuOpen = false">
        </div>
      </div>
    </div>
  </header>
</template>
