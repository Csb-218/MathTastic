<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import NavbarStudent from '@/components/blocks/navigation/NavbarStudent.vue'
import BalanceScale from './games/BalanceScale.vue'
import { useRoute } from 'vue-router'
import { getGameById } from "@/services/GameService"
import {
  getProgressByStudentUid,
  createProgress,
} from '@/services/FireStoreService'
import type { Game } from '@/types/game'
import type { game_progress, progress_object } from '@/types/progress'
import { useAuthStore } from "@/stores/authStore"

const loading = ref(false)
const { params } = useRoute();

const gameId: string = params.id as string
const currentGame = ref<Game | null>(null)
const progressDocId = ref<string>('')
const levels = computed(() => currentGame.value?.activities.length)

const { uid } = useAuthStore()

const dummyGames: Game[] = [
  {
    id: "1",
    title: "Balance the Scale",
    description: "Learn addition and subtraction by balancing weights on a scale",
    image: "https://scoonews.com/wp-content/uploads/2022/07/cover15851292261585129226.jpg",
    difficulty: "easy",
    age_range: "6-8",
    activities: [], // Initialize as empty array
    target_range: [1, 20],
    total_points: 100,
    template: false
  },
  {
    id: '2',
    title: "Number Ninja",
    description: "Slice through numbers to master multiplication tables",
    image: "https://store-images.s-microsoft.com/image/apps.65264.13510798882430817.b10ab5df-3d92-47ad-9d56-96b15f73d63f.f3743b21-d1d9-4f19-9f7f-042b30214eef?mode=scale&q=90&h=1080&w=1920",
    difficulty: "medium",
    age_range: "8-10",
    activities: [],
    target_range: [1, 50],
    total_points: 150,
    template: false
  },
  {
    id: '3',
    title: "Fraction Factory",
    description: "Build and compare fractions in this fun factory game",
    image: "https://storage.googleapis.com/ltkcms.appspot.com/fs/wfa/images/cover/wordsmith.base?v=1599144875",
    difficulty: "hard",
    age_range: "9-11",
    activities: [],
    target_range: [1, 100],
    total_points: 200,
    template: false
  }
]

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
    loading.value = true
    // Fetch the game data using the gameId from the route
    const game = await getGameById(gameId)
    // Set the current game
    currentGame.value = game
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})

watch(currentGame, async () => {

  if (currentGame.value) {

    const progress: progress_object | null = await getProgressByStudentUid(uid, currentGame.value.id)

    // if no progress is available
    if (!progress) {
      // create a new game progress
      const new_game_progress: game_progress = {
        game_id: currentGame.value.id,
        current_level: 0,
        points_gained: 0,
        total_levels: currentGame.value.activities.length,
        total_points: currentGame.value.total_points,
      }
      // create progress in Firestore
      // and update the progress document ID in the store
      const progress_id = await createProgress(uid, new_game_progress)
      progressDocId.value = progress_id
    }
    // if progress is available
    else {
      progressDocId.value = progress.id
    }
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
          <BalanceScale v-if="currentGame && progressDocId" :currentGame="currentGame" :progress_id="progressDocId" />
        </div>
      </section>

      <!-- About the Game Section -->
      <section class="bg-white rounded-xl shadow-lg p-6">
        <div class="flex justify-between items-start mb-4 ">

          <h2 class="text-2xl font-bubblegum text-gray-800">About this Game</h2>

          <button @click="shareGame"
            class="bg-blue-500 hover:bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-lg font-bubblegum flex items-center gap-2"
            aria-label="Share Game">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
            </svg>
            <span class="hidden sm:inline">Share Game</span>
          </button>

        </div>
        <p class="text-gray-600 mt-2">{{ currentGame?.description }}</p>
        <div class="flex gap-4 mt-4 w-full">
          <div class="bg-amber-100 px-4 py-2 rounded-full">
            <span class="font-bubblegum text-amber-700">
              Levels: {{ levels }}
            </span>
          </div>
          <div class="bg-amber-100 px-4 py-2 rounded-full">
            <span class="font-bubblegum text-amber-700">
              Age: {{ }} 3-7
            </span>
          </div>
          <div class="bg-amber-100 px-4 py-2 rounded-full">
            <span class="font-bubblegum text-amber-700">
              Points: {{ currentGame?.total_points }}
            </span>
          </div>
        </div>

      </section>

      <!-- Other Games Section -->
      <section class="bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-2xl font-bubblegum text-gray-800 mb-4">More Fun Games</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div v-for="game in dummyGames" :key="game.id"
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
