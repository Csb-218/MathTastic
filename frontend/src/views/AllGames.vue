<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Game } from '@/types/game'
import { getAllGames } from '@/services/GameService'
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue'

const games = ref<Game[]>([])
const loading = ref(true)
const error = ref('')


const balanceScaleBG = "https://scoonews.com/wp-content/uploads/2022/07/cover15851292261585129226.jpg"

const fetchGames = async () => {
  games.value = await getAllGames()
  loading.value = false
}


onMounted(() => {
  fetchGames()
})
</script>

<template>
  <NavbarStandard />
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white mt-6 py-6">


    <main class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-bubblegum text-amber-500 text-center mb-8 animated-glow">
        Math Games
      </h1>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-amber-500"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center text-red-500 font-bubblegum text-xl">
        {{ error }}
      </div>

      <!-- Games Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="game in games" :key="game.id"
          class="bg-white rounded-xl shadow-lg hover:shadow-xl hover:scale-105 delay-75 transition-transform duration-300">
          <div class="relative aspect-w-16 aspect-h-9 rounded-t-xl overflow-hidden">
            <img :src="game.image || balanceScaleBG" :alt="game.title" class="object-cover w-full h-full" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="bg-amber-500 text-white px-3 py-1 rounded-full text-sm font-bubblegum">
                {{ game.difficulty }}
              </span>
            </div>
          </div>

          <div class="p-6">
            <h2 class="text-2xl font-bubblegum text-gray-800 mb-2">{{ game.title }}</h2>
            <p class="text-gray-600 mb-4">{{ game.description }}</p>

            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500 font-bubblegum">
                Age {{ game.age_range }}
              </span>
              <button
                class="bg-amber-500 hover:bg-amber-600 text-white font-bubblegum py-2 px-4 rounded-lg transition-colors duration-300"
                @click="$router.push(`/play/${game.id}`)">
                Play Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.animated-glow {
  animation: glowing 2s ease-in-out infinite;
}

@keyframes glowing {

  0%,
  100% {
    text-shadow: 0 0 10px rgba(245, 158, 11, 0.7),
      0 0 20px rgba(245, 158, 11, 0.7);
  }

  50% {
    text-shadow: 0 0 20px rgba(245, 158, 11, 0.9),
      0 0 30px rgba(245, 158, 11, 0.9);
  }
}

.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%;
}

.aspect-w-16>* {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
