<script setup lang="ts">
import type { Game } from '@/types/game'

defineProps<{
  games: Game[]
}>()
</script>

<template>
  <h2 class="text-4xl sm:text-5xl text-center font-bold font-[Fredoka] text-gray-900 mb-4 sm:mb-6">Our Games</h2>
  <p class="text-lg py-10 sm:text-xl text-center text-gray-600 mb-6 sm:mb-8">
    Where Math Meets Play: Help Kids Master Addition Through Interactive Balance Challenges!
  </p>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
    <div 
      v-for="game in games" 
      :key="game.id"
      class="overflow-hidden bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300"
    >
      <figure>
        <img :src="game.image" :alt="game.title" class="aspect-video w-full object-cover" />
      </figure>
      <div class="p-6">
        <header class="mb-4">
          <h3 class="text-xl font-medium text-slate-700">{{ game.title }}</h3>
          <p class="text-sm text-slate-400">{{ game.level }} | {{ game.ageRange }}</p>
        </header>
        <p class="text-slate-600">{{ game.description }}</p>
      </div>
    </div>
  </div>
</template>