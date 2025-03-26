<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Game } from '@/types/game'
import NavbarStudent from '@/components/blocks/navigation/NavbarStudent.vue'
import BalanceScale from './games/BalanceScale.vue'

const loading = ref(false)
const currentGame = ref<Game | null>(null)
const similarGames = ref<Game[]>([
  {
    id: 2,
    title: "Number Ninja",
    description: "Master multiplication with this exciting ninja-themed game!",
    image: "https://placehold.co/600x400/purple/white?text=Number+Ninja",
    level: "beginner",
    ageRange: "6-8",
    activities: [], // Initialize as empty array
    targetRange: [1, 20],
    totalPoints: 120,
    template: false
  },
  {
    id: 3,
    title: "Math Quest",
    description: "Embark on an adventure through the world of addition!",
    image: "https://placehold.co/600x400/blue/white?text=Math+Quest",
    level: "beginner",
    ageRange: "6-8",
    activities: [],
    targetRange: [1, 15],
    totalPoints: 90,
    template: false
  },
  {
    id: 4,
    title: "Addition Explorer",
    description: "Discover the fun in adding numbers together!",
    image: "https://placehold.co/600x400/green/white?text=Addition+Explorer",
    level: "beginner",
    ageRange: "6-8",
    activities: [],
    targetRange: [1, 25],
    totalPoints: 110,
    template: false
  }
])

const shareGame = () => {
  if (navigator.share) {
    navigator.share({
      title: currentGame.value?.title,
      text: currentGame.value?.description,
      url: window.location.href
    })
  }
}

onMounted(async () => {
  try {
    // TODO: Replace with actual API call
    loading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000))
    currentGame.value = {
      id: 1,
      title: "Balance the Scale",
      description: "Learn addition and subtraction by balancing weights on a scale",
      image: "https://placehold.co/600x400/orange/white?text=Balance+Scale",
      level: "beginner",
      ageRange: "6-8",
      activities: [],
      targetRange: [1, 20],
      totalPoints: 100,
      template: false
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-amber-50 to-white mt-16">
    <NavbarStudent />

    <main class="container mx-auto px-4 py-8 space-y-8">
      <!-- Game Window Section -->
      <section class="bg-white rounded-xl shadow-lg p-6 min-h-[300px]">
        <h1 class="text-3xl font-bubblegum text-amber-500 mb-4">
          {{ currentGame?.title }}
        </h1>
        <div class="aspect-w-16 aspect-h-9 bg-gray-100 rounded-lg">
          <!-- Game content will go here -->
          <!-- <div class="flex items-center justify-center">
                        <p class="text-gray-500 font-bubblegum">Game Loading...</p>
                    </div> -->
          <BalanceScale />
        </div>
      </section>

      <!-- About the Game Section -->
      <section class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-2xl font-bubblegum text-gray-800">About this Game</h2>
            <p class="text-gray-600 mt-2">{{ currentGame?.description }}</p>

            <div class="flex gap-4 mt-4">
              <div class="bg-amber-100 px-4 py-2 rounded-full">
                <span class="font-bubblegum text-amber-700">
                  Level: {{ currentGame?.level }}
                </span>
              </div>
              <div class="bg-amber-100 px-4 py-2 rounded-full">
                <span class="font-bubblegum text-amber-700">
                  Age: {{ currentGame?.ageRange }}
                </span>
              </div>
              <div class="bg-amber-100 px-4 py-2 rounded-full">
                <span class="font-bubblegum text-amber-700">
                  Points: {{ currentGame?.totalPoints }}
                </span>
              </div>
            </div>
          </div>

          <button @click="shareGame"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-bubblegum flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z">
              </path>
            </svg>
            Share Game
          </button>
        </div>
      </section>

      <!-- Other Games Section -->
      <section class="bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-2xl font-bubblegum text-gray-800 mb-4">More Fun Games</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div v-for="game in similarGames" :key="game.id"
            class="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="aspect-w-16 aspect-h-9 bg-gray-200 rounded-lg mb-2">
              <img :src="game.image" :alt="game.title" class="object-cover w-full h-full rounded-lg">
            </div>
            <h3 class="font-bubblegum text-gray-700">{{ game.title }}</h3>
            <p class="text-sm text-gray-500">{{ game.description }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
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
