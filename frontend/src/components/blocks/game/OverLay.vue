<template>

  <div v-if="isCompleted" class="absolute inset-0 flex flex-col p-2 items-center justify-center bg-white/90">
    <PlayCircleIcon class="h-12 w-12 mb-4 text-amber-600" />
    <h2 class="font-bubblegum text-2xl text-amber-600 mb-2">Balance Scale</h2>
    <p class="font-bubblegum text-gray-600 mb-6 px-4 text-center">
      Hurray ! You have completed all levels
    </p>
    <!-- play game button -->
    <button @click="restartGame(container)"
      class="bg-amber-500 hover:bg-amber-600 text-white font-bubblegum py-3 px-8 rounded-full shadow-lg transform transition hover:scale-105">
      Restart Game
    </button>
  </div>


  <div v-else class="absolute inset-0 flex flex-col p-2 items-center justify-center bg-white/90">
    <PlayCircleIcon class="h-12 w-12 mb-4 text-amber-600" />
    <h2 class="font-bubblegum text-2xl text-amber-600 mb-2">Balance Scale</h2>
    <p class="font-bubblegum text-gray-600 mb-6 px-4 text-center">
      Tap Play to start in fullscreen mode
    </p>
    <!-- play game button -->
    <button @click="startGame(container)"
      class="bg-amber-500 hover:bg-amber-600 text-white font-bubblegum py-3 px-8 rounded-full shadow-lg transform transition hover:scale-105">
      Play Game
    </button>
  </div>
</template>
<script lang="ts" setup>
import { PlayCircleIcon } from 'lucide-vue-next'

defineProps<{
  startGame: (container: HTMLElement | null) => void
  container: HTMLElement | null
  isCompleted: boolean
  restartGame: (container: HTMLElement | null) => void
}>()
</script>
