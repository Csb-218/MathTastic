<script setup lang="ts">
import calculator_logo from "@/assets/icons/calculator_logo.png"

</script>

<template>
  <nav class="bg-white shadow-md fixed w-full top-0 z-50">
    <div class="max-w-screen-2xl mx-auto px-2 sm:px-4 lg:px-6">
      <div class="flex justify-between h-16 ">
        <div class="flex-shrink-0 flex items-center gap-x-2">
          <img :src="calculator_logo" alt="MathTastic" class="h-8 w-8 " />
          <p class="text-2xl sm:text-4xl  font-bubblegum text-amber-500">MathTastic</p>
        </div>
        <div class="hidden sm:flex items-center gap-x-4">
          <RouterLink to="/educator" class="text-gray-700 hover:text-blue-600 transition-colors">For Educators
          </RouterLink>
          <RouterLink to="/student" class="text-gray-700 hover:text-blue-600 transition-colors">Students</RouterLink>
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
