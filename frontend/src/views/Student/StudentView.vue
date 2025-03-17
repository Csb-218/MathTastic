<script setup lang="ts">
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import NavbarStudent from '@/components/blocks/navigation/NavbarStudent.vue'
import { useAuthStore } from '@/stores/authentication'

const authState = useAuthStore()

const studentStats = ref({
  totalPoints: 520,
  gamesCompleted: 15,
  currentLevel: 3,
  badges: ['Beginner', 'QuickGrasper']
})

onMounted(() => {
  gsap.from('.auth-form', {
    opacity: 0,
    y: 20,
    duration: 0.6,
    ease: 'power2.out'
  })
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white">
    <NavbarStudent />

    <!-- Auth Form -->
    <main class="pt-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <!-- Welcome Section -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-fredoka font-bold text-gray-900">Welcome Back, {{ authState.name }} !</h1>
          <p class="mt-2 text-gray-600">Ready to continue your math adventure?</p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Total Points</h3>
            <p class="text-2xl font-bold text-amber-500">{{ studentStats.totalPoints }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Games Completed</h3>
            <p class="text-2xl font-bold text-amber-500">{{ studentStats.gamesCompleted }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Current Level</h3>
            <p class="text-2xl font-bold text-amber-500">{{ studentStats.currentLevel }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Badges Earned</h3>
            <p class="text-2xl font-bold text-amber-500">{{ studentStats.badges.length }}</p>
          </div>
        </div>

        <!-- Current Games Section -->
        <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Continue Learning</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Game cards would go here -->
            <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <h3 class="font-semibold">Addition Adventure</h3>
              <p class="text-sm text-gray-600">Level 3 - In Progress</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>