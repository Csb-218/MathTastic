<script setup lang="ts">
import { ref } from 'vue'
import NavbarEducator from '@/components/blocks/navigation/NavbarEducator.vue';
import { RouterView } from 'vue-router';
const teacherStats = ref({
  totalStudents: 25,
  activeGames: 3,
  averageProgress: 78,
  completionRate: 85
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white">
    <NavbarEducator />

    <RouterView />



    <main class="pt-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <!-- Welcome Section -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-fredoka font-bold text-gray-900">Educator Dashboard</h1>
          <p class="mt-2 text-gray-600">Manage your classes and track student progress</p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Total Students</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.totalStudents }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Active Games</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.activeGames }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Average Progress</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.averageProgress }}%</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Completion Rate</h3>
            <p class="text-2xl font-bold text-amber-500">{{ teacherStats.completionRate }}%</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
            <div class="space-y-4">
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                Create New Game
              </button>
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                Assign Activities
              </button>
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                View Reports
              </button>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <div class="space-y-4">
              <!-- Activity items would go here -->
              <div class="border-b pb-2">
                <p class="font-medium">Math Quiz Completed</p>
                <p class="text-sm text-gray-600">15 students completed Level 2</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>