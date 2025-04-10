<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const teacherStats = ref({
  totalStudents: 25,
  activeGames: 3,
  averageProgress: 78,
  completionRate: 85
})

const navigateTo = (route: string) => {
  router.push(`/educator/${route}`)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white">

    <main class="pt-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <!-- Welcome Section -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-fredoka font-bold text-gray-900">Welcome Back, Educator!</h1>
          <p class="mt-2 text-gray-600">Manage your games and track student progress</p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h3 class="text-lg font-semibold text-gray-700">Total Students</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.totalStudents }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h3 class="text-lg font-semibold text-gray-700">Active Games</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.activeGames }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h3 class="text-lg font-semibold text-gray-700">Average Progress</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.averageProgress }}%</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <h3 class="text-lg font-semibold text-gray-700">Completion Rate</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.completionRate }}%</p>
          </div>
        </div>

        <!-- Main Actions -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <!-- Games Management -->
          <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
            <div class="text-center mb-4">
              <div class="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg class="w-8 h-8 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
                </svg>
              </div>
              <h2 class="text-xl font-semibold text-gray-900">Games</h2>
            </div>
            <div class="space-y-3">
              <button @click="navigateTo('games')"
                class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors">
                View Games
              </button>
              <button
                class="w-full py-2 px-4 bg-white border border-amber-500 text-amber-500 rounded-lg hover:bg-amber-50 transition-colors">
                Create New Game
              </button>
            </div>
          </div>

          <!-- Progress Tracking -->
          <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
            <div class="text-center mb-4">
              <div class="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg class="w-8 h-8 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h2 class="text-xl font-semibold text-gray-900">Progress</h2>
            </div>
            <button @click="navigateTo('progress')"
              class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors">
              View Progress
            </button>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <div class="space-y-4">
              <div class="border-b pb-2">
                <p class="font-medium">Math Quiz Updated</p>
                <p class="text-sm text-gray-600">2 new activities added</p>
                <p class="text-xs text-gray-400">2 hours ago</p>
              </div>
              <div class="border-b pb-2">
                <p class="font-medium">Student Progress</p>
                <p class="text-sm text-gray-600">15 students completed Level 2</p>
                <p class="text-xs text-gray-400">Yesterday</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
