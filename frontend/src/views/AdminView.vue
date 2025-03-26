<script setup lang="ts">
import { ref } from 'vue'
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue';

const adminStats = ref({
  totalUsers: 1250,
  activeEducators: 45,
  totalStudents: 1200,
  totalGames: 25
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white">
    <NavbarStandard />

    <main class="pt-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <!-- Welcome Section -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-fredoka font-bold text-gray-900">Admin Dashboard</h1>
          <p class="mt-2 text-gray-600">System Overview and Management</p>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Total Users</h3>
            <p class="text-2xl font-bold text-amber-500">{{ adminStats.totalUsers }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Active Educators</h3>
            <p class="text-2xl font-bold text-amber-500">{{ adminStats.activeEducators }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Total Students</h3>
            <p class="text-2xl font-bold text-amber-500">{{ adminStats.totalStudents }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm">
            <h3 class="text-lg font-semibold text-gray-700">Total Games</h3>
            <p class="text-2xl font-bold text-amber-500">{{ adminStats.totalGames }}</p>
          </div>
        </div>

        <!-- Admin Tools -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">System Management</h2>
            <div class="space-y-4">
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                User Management
              </button>
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                Content Management
              </button>
              <button class="w-full py-2 px-4 bg-amber-500 text-white rounded-lg hover:bg-amber-600">
                System Settings
              </button>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">System Metrics</h2>
            <div class="space-y-4">
              <!-- Metrics would go here -->
              <div class="border-b pb-2">
                <p class="font-medium">System Status: Active</p>
                <p class="text-sm text-gray-600">All services operating normally</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>