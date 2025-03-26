<template>

  <div ref="gameContainer"
    class="game-container  bg-[url(@/assets/backgrounds/rainbow_landscape.jpg)] bg-cover text-center p-5 bg-[#f5f5d5] font-sans relative ">

    <!-- Loading state -->
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/50">
      <div class="loading-spinner">Loading...</div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="absolute inset-0 flex items-center justify-center bg-white/50">
      <div class="text-red-500">{{ error }}</div>
    </div>

    <!-- Mobile View with Play Button -->
    <div v-else-if="isMobileView && !isPlaying"
      class="absolute inset-0 flex flex-col p-2 items-center justify-center bg-white/90">
      <PlayCircleIcon class="h-12 w-12 mb-4 text-amber-600" />
      <h2 class="font-bubblegum text-2xl text-amber-600 mb-2">Balance Scale</h2>
      <p class="font-bubblegum text-gray-600 mb-6 px-4 text-center">
        Tap Play to start in fullscreen mode
      </p>
      <!-- play game button -->
      <button @click="startGame(gameContainer)"
        class="bg-amber-500 hover:bg-amber-600 text-white font-bubblegum py-3 px-8 rounded-full shadow-lg transform transition hover:scale-105">
        Play Game
      </button>
    </div>

    <!-- Game content -->
    <template v-else>

      <!-- Exit game button -->
      <button @click="exitGame" class="absolute top-4 right-4 p-2 text-white  " title="Exit fullscreen">
        <img :src="exit" alt="exit" class="w-10 h-10" />
      </button>
      <!-- Minimize -->
      <button @click="toggleFullscreen(gameContainer)"
        class="absolute top-4 left-4 p-1 text-white bg-slate-800 rounded  " title="Minimize">
        <Minimize class="w-10 h-10" />
      </button>

      <!-- Level board -->
      <span class="absolute top-4 left-1/2 -translate-x-1/2 p-2 text-white">
        <img :src="level_board" alt="level_board" class="h-20" />
        <p class="z-50 absolute top-1/3 left-1/2 -translate-x-1/2 font-bubblegum text-2xl ">Level 1</p>
      </span>

      <!-- balance status -->
      <div v-if="showMessage"
        class="absolute -translate-x-1/2 top-1/4 left-1/2 p-4 text-yellow-400 bg-slate-900/80 rounded-lg transform transition-all duration-300 ease-in-out"
        :class="{ 'scale-100 opacity-100': showMessage, 'scale-95 opacity-0': !showMessage }">
        <p class="font-bubblegum text-2xl">{{ balanceStatus }}</p>
      </div>

      <!-- Balance scale -->
      <div class=" flex justify-center my-5 absolute h-2/4 bottom-0 left-1/2 -translate-x-1/2"
        :class="isFullScreen ? ' w-full' : ' w-1/2'">
        <!-- Fixed vertical stand -->
        <img :src="stand" alt="stand" class="stand h-full drop-shadow-lg" />
        <!-- Rotating beam and baskets -->
        <div class="beam w-[70%] sm:w-[60%] md:w-[60%] lg:w-1/2 cursor-grabbing"
          :style="{ transform: `rotate(${tiltAngle}deg)` }">
          <img :src="nut" alt="nut"
            class="absolute top-[10px] left-1/2 -translate-x-1/2 w-[30px] h-[30px] z-50 bg-amber-300 rounded-full border-0">
          <!-- Horizontal beam -->
          <div class="beam-bar absolute top-[20px] left-0 w-full h-[10px] bg-[#999] rounded-[5px]"></div>
          <div
            class="pan left-pan absolute top-[40px] -left-16 w-[150px] h-[150px] flex flex-wrap items-end py-4 justify-center"
            @drop="drop($event, 'left')" @dragover="allowDrop">
            <div v-for="obj in leftPanObjects" :key="obj.id" class="object-container">
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " :style="getObjectStyle(obj)"
                draggable="true" @dragstart="drag($event, obj)">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              </div>
            </div>
            <p class="absolute -bottom-7 font-bubblegum text-white text-lg">{{ leftWeight }}</p>
          </div>
          <div
            class="pan right-pan absolute top-[40px] -right-16 w-[150px] h-[150px] flex flex-wrap items-end py-4 justify-center"
            @drop="drop($event, 'right')" @dragover="allowDrop">
            <div v-for="obj in rightPanObjects" :key="obj.id" class="object-container">
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " :style="getObjectStyle(obj)"
                draggable="true" @dragstart="drag($event, obj)">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              </div>

            </div>
            <p class="absolute -bottom-7 font-bubblegum text-white text-lg">{{ rightWeight }}</p>
          </div>
        </div>
      </div>

      <!-- weighing objects -->
      <div class="weights my-5 absolute left-1/2 -translate-x-1/2" :class="isFullScreen ? 'bottom-10' : 'bottom-4'">
        <div class="flex justify-center gap-2 ">
          <div v-for="obj in availableObjects" :key="obj.id"
            class="object-container flex flex-col items-center m-1 cursor-grabbing">
            <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " :style="getObjectStyle(obj)"
              draggable="true" @dragstart="drag($event, obj)">
              <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              <p class="text-white font-bubblegum">{{ obj.weight }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- game control buttons -->

      <!-- left controls -->
      <div class="flex flex-col justify-center gap-1 absolute left-5 bottom-14 ">
        <button @click="resetGame" class="p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="reload" alt="reload" class="w-10 h-10" />
        </button>
        <button @click="resetGame" class="p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="music" alt="reload" class="w-10 h-10" />
        </button>
      </div>

      <!-- right controls -->
      <div class="flex flex-col justify-center gap-1 absolute right-5 bottom-14 ">
        <button @click="resetGame" class=" p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="more_games" alt="reload" class="w-10 h-10" />
        </button>
        <button @click="resetGame" class=" p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="leaderboard" alt="reload" class="w-10 h-10" />
        </button>

      </div>


    </template>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useEventListener } from '@vueuse/core'
import { storeToRefs } from 'pinia'

// Services
// import { gameService } from '@/services/gameService'

//store
import { useBalanceScaleStore } from '@/stores/balanceScale'

// assets
import { Minimize } from 'lucide-vue-next';
import { PlayCircleIcon } from 'lucide-vue-next'
import nut from "@/assets/game/nut_dark.svg"
import stand from "@/assets/game/Stand.png"
import reload from "@/assets/game/reload.png"
import exit from "@/assets/game/exit.png"
import leaderboard from "@/assets/game/leaderboard.png"
import more_games from "@/assets/game/more_games.png"
import music from "@/assets/game/music.png"
import level_board from "@/assets/game/level_board.png"
import appleIcon from "@/assets/game/apple.svg"
import bananaIcon from "@/assets/game/banana.svg"
import orangeIcon from "@/assets/game/orange.svg"
// helpers
import { getObjectStyle } from "@/lib/helpers"

// State
const gameContainer = ref<HTMLElement | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const {
  tiltAngle,
  leftPanObjects,
  rightPanObjects,
  leftWeight,
  rightWeight,
  availableObjects,
  balanceStatus,
  showMessage,
  isPlaying,
  isFullScreen } = storeToRefs(useBalanceScaleStore())

const {
  initGameObjects,
  fullScreenChange,
  exitGame,
  startGame,
  resetGame,
  drop,
  drag,
  allowDrop,
  toggleFullscreen
} = useBalanceScaleStore()

// Sample game data
const sampleGameData = {
  objects: [
    {
      id: '1',
      weight: 2,
      color: '#FF6B6B',
      type: 'apple',
      image: appleIcon,
      location: "available" as const
    },
    {
      id: '2',
      weight: 3,
      color: '#FFD93D',
      type: 'banana',
      image: bananaIcon,
      location: "available" as const
    },
    {
      id: '3',
      weight: 4,
      color: '#FF9F45',
      type: 'orange',
      image: orangeIcon,
      location: "available" as const
    },
    {
      id: '4',
      weight: 2,
      color: '#FF6B6B',
      type: 'apple',
      image: appleIcon,
      location: "available" as const
    },
    {
      id: '5',
      weight: 3,
      color: '#FFD93D',
      type: 'banana',
      image: bananaIcon,
      location: "available" as const
    }
  ]
}

// Fetch game data
const fetchGameData = async () => {
  try {
    loading.value = true
    // Simulate API call with setTimeout
    await new Promise(resolve => setTimeout(resolve, 1000))
    initGameObjects(sampleGameData.objects)
  } catch (err) {
    error.value = 'Failed to load game objects'
    console.error(err)
  } finally {
    console.log('Objects loaded:', availableObjects)
    loading.value = false
  }
}

// Methods
const handleResize = () => {
  isMobileView.value = window.innerWidth < 768
}

// Event listeners
useEventListener(window, 'resize', handleResize)
useEventListener(document, 'fullscreenchange', fullScreenChange)

// viewport check
const isMobileView = ref(window.innerWidth < 768)

onMounted(async () => {
  await fetchGameData()
})

onUnmounted(() => {
  exitGame()
})


</script>

<style scoped>
.beam {
  position: relative;
  top: -25%;
  transform-origin: center 20px;
  transition: transform 0.5s ease;
}

.stand {
  position: absolute;
  top: -20%;
  left: 50%;
  transform: translateX(-50%);
}

.left-pan .ball,
.right-pan .ball {
  position: sticky;
  z-index: -10;
  bottom: 10px;
}

/* Basket image for the pans */
.left-pan,
.right-pan {
  background-image: url("@/assets/game/weighing_pan.svg");
  /* Adjust the path to your basket image */
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  top: 28px;

}

/* Two chains for the left pan forming a triangle */


.left-pan::before {
  left: 50%;
  transform: rotate(-30deg);
}

.left-pan::after {
  left: 50%;
  transform: rotate(30deg);
}

/* Two chains for the right pan forming a triangle */


.right-pan::before {
  left: 50%;
  transform: rotate(-30deg);
}

.right-pan::after {
  left: 50%;
  transform: rotate(30deg);
}

.green {
  background-color: #008000;
}

.yellow {
  background-color: #ffff00;
}

.red {
  background-color: #ff0000;
}

.white {
  background-color: #ffffff;
  border: 1px solid #000;
}

.blue {
  background-color: #0000ff;
}


.game-container:fullscreen {
  /* background-image: url("@/assets/backgrounds/rainbow_landscape.jpg");
  background-size: cover; */
  /* display: flex; */
  flex-direction: column;
  justify-content: center;
  align-items: center;
}


.game-object {
  transition: transform 0.2s ease;
}

.game-object:hover {
  transform: scale(1.1);
}

.loading-spinner {
  @apply text-amber-600 text-xl font-bold;
}

/* Add these styles */
.game-container {
  height: 100vh;
  width: 100vw;
}

.game-container:fullscreen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-size: cover;
  background-position: center;
}

/* Add to your <style> section */
.transform {
  transition: all 0.3s ease-in-out;
}

@keyframes bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

.scale-win {
  animation: bounce 0.5s ease-in-out;
}
</style>
