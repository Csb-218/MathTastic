<script setup lang="ts">

</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bubblegum text-gray-800 mb-8">Student Progress</h1>

    <div class="bg-white rounded-xl shadow-lg p-6">
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="bg-amber-50">
            <tr>
              <th class="px-6 py-3 text-left">Student</th>
              <th class="px-6 py-3 text-left">Game</th>
              <th class="px-6 py-3 text-left">Level</th>
              <th class="px-6 py-3 text-left">Points</th>
              <th class="px-6 py-3 text-left">Last Played</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <!-- Progress data rows -->
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
