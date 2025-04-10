<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Game } from '@/types/game'
import { getAllGames } from '@/services/GameService'

const games = ref<Game[]>([])

onMounted(async () => {
  // Fetch games data
  games.value = await getAllGames()

})
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bubblegum text-gray-800">Games Library</h1>
      <router-link to="/educator/games/create"
        class="bg-amber-500 text-white px-6 py-2 rounded-full hover:bg-amber-600">
        Create New Game
      </router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Game cards -->
      <div v-for="game in games" :key="game.id" class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
        <h3 class="text-xl font-bubblegum text-gray-800 mb-2">{{ game.title }}</h3>
        <!-- game cover -->
        <div class="relative aspect-w-16 aspect-h-9 rounded-lg overflow-hidden mb-4">
          <img src="https://scoonews.com/wp-content/uploads/2022/07/cover15851292261585129226.jpg" :alt="game.title"
            class="object-cover w-full h-full" />
        </div>
        <p class="text-gray-600 mb-4">{{ game.description }}</p>
        <router-link :to="`/educator/games/${game.id}/create`" class="text-amber-500 hover:text-amber-600">
          Create Activity →
        </router-link>
      </div>
    </div>
  </div>
</template>
