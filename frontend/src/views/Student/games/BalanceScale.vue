<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useEventListener } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import type { Game } from '@/types/game'
import type { game_progress } from '@/types/progress'
import { createWeighingObjectsFromActivity } from '@/lib/helpers'
import { doc, onSnapshot } from 'firebase/firestore'
import { db } from '@/config/firebaseConfig'
import { updateProgress, resetProgress } from '@/services/FireStoreService'
//store
import { useBalanceScaleStore } from '@/stores/Gameplay/BalanceScale/balanceScale'
import { useAuthStore } from '@/stores/authStore'
// assets
import { Minimize } from 'lucide-vue-next';
import OverLay from '@/components/blocks/game/OverLay.vue'
import { exit, level_board, music, nut, reload, stand, points_board } from "@/assets/game"
import { SoundService } from '@/services/SoundService'
import LevelComplete from '@/components/blocks/game/LevelComplete.vue';
import { congratulations_character } from '@/assets/game'

// props
const { currentGame, progress_id } = defineProps<{
  currentGame: Game
  progress_id: string
}>()

// States
const currentLevel = ref<number>(1)
const totalPoints = ref<number>(0)
const gameContainer = ref<HTMLElement | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
// viewport check
const isMobileView = ref(window.innerWidth < 768)


// store states , getters and actions
const {
  tiltAngle,
  leftPanObjects,
  rightPanObjects,
  leftWeight,
  rightWeight,
  availableObjects,
  showMessage,
  isPlaying,
  hasWon,
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
  toggleFullscreen,
  handleTouchStart,
  handleTouchMove,
  handleTouchEnd
} = useBalanceScaleStore()

const { uid } = storeToRefs(useAuthStore())


// Methods

// resize
const handleResize = () => {
  isMobileView.value = window.innerWidth < 768
}
// restart game
const restartGame = async () => {
  await resetProgress(uid.value, progress_id)
  console.log("restart game successfully")
}

// Fetch game state
const fetchGameState = async () => {

  try {

    onSnapshot(doc(db, `/progress/${uid.value}/games_played/${progress_id}`), (doc) => {
      const data = doc.data()
      if (!data) {
        console.error('No such document!')
        return
      }

      currentLevel.value = data.current_level
      totalPoints.value = data.points_gained

      const level = data.current_level
      const hasNextLevel = data.total_levels > level
      const hasCompleted = (data.total_levels === level) && (data.points_gained === data.total_points)


      if (hasNextLevel) {
        // init next level
        const activity_objects = createWeighingObjectsFromActivity(currentGame.activities[level])
        initGameObjects(activity_objects)
      }

      if (hasCompleted) {
        return
      }

    })

  } catch (err) {
    error.value = 'Failed to load game objects'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// computed values

// points gained
const pointsGained = computed(() => {
  return currentGame.activities[currentLevel.value].points
})
// check if the game is completed
const isCompleted = computed(() => {
  const value = currentLevel.value === currentGame.activities.length
  if (value) SoundService.play('win')
  return value
})

// handle win
watch(
  hasWon,
  async () => {
    if (hasWon.value) {
      showLevelComplete.value = true;
    }
  }
)

watch(showMessage, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      showMessage.value = false
    }, 2000)
  }
})

// reactive variables
const showLevelComplete = ref(false);
const successMessage = computed(() =>
  ` ${currentGame.activities[currentLevel.value].success_feedback}!`
);

// handler for level completion
const handleLevelComplete = async () => {
  showLevelComplete.value = false;
  const updates: Partial<game_progress> = {
    points_gained: pointsGained.value,
    current_level: ++currentLevel.value,
  };
  await updateProgress(uid.value, progress_id, updates);
};

// Event listeners
useEventListener(window, 'resize', handleResize)
useEventListener(document, 'fullscreenchange', fullScreenChange)


onMounted(async () => {
  await fetchGameState()
})

onUnmounted(() => {
  exitGame()
})


</script>

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
    <OverLay v-else-if="(isMobileView && !isPlaying) || isCompleted" :start-game="startGame" :restartGame="restartGame"
      :container="gameContainer" :isCompleted="isCompleted" />

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

      <div
        class="absolute top-4 left-1/2 -translate-x-1/2 flex items-center gap-3 lg:ml-11 lg:scale-100 scale-90 ml-3 ">
        <!-- Level board -->
        <span class="relative">
          <img :src="level_board" alt="level_board" class="h-20" />
          <p class="z-50 absolute top-1/3 left-1/2 -translate-x-1/2 font-bubblegum lg:text-2xl text-xl text-white">
            Level {{ currentLevel + 1 }}
          </p>
        </span>

        <!-- Score board -->
        <span class="relative">
          <img :src="points_board" alt="score_board" class="h-20" />
          <div class="z-50 absolute top-1/3 left-1/2 -translate-x-1/2 font-bubblegum text-white">
            <p class="text-2xl -mt-1">{{ totalPoints }}</p>
            <p class="text-xs -mt-2">points</p>
          </div>
        </span>
      </div>

      <!-- Balance scale -->
      <div
        class=" flex justify-center my-5 absolute h-2/4 lg:bottom-0 bottom-6 lg:scale-100 scale-90 left-1/2 -translate-x-1/2"
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
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " draggable="true"
                @dragstart="drag($event, obj)" @touchstart="(e: TouchEvent) => handleTouchStart(e, obj)"
                @touchmove="(e: TouchEvent) => handleTouchMove(e)" @touchend="handleTouchEnd">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              </div>
            </div>
            <p class="absolute -bottom-7 font-bubblegum text-white text-lg">{{ leftWeight }}</p>
          </div>
          <div
            class="pan right-pan absolute top-[40px] -right-16 w-[150px] h-[150px] flex flex-wrap items-end py-4 justify-center"
            @drop="drop($event, 'right')" @dragover="allowDrop">
            <div v-for="obj in rightPanObjects" :key="obj.id" class="object-container">
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " draggable="true"
                @dragstart="drag($event, obj)" @touchstart="(e: TouchEvent) => handleTouchStart(e, obj)"
                @touchmove="(e: TouchEvent) => handleTouchMove(e)" @touchend="handleTouchEnd">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              </div>

            </div>
            <p class="absolute -bottom-7 font-bubblegum text-white text-lg">{{ rightWeight }}</p>
          </div>
        </div>
      </div>

      <!-- weighing objects -->
      <div class=" absolute left-1/2 -translate-x-1/2 transition-all duration-300 w-9/12  "
        :class="isFullScreen ? 'bottom-6' : 'bottom-4'">
        <div class="p-4 rounded-lg   ">
          <div class="flex flex-wrap lg:gap-4 gap-2 justify-center">
            <div v-for="obj in availableObjects" :key="obj.id"
              class="flex flex-col items-center  rounded-lg p-2 cursor-grabbing hover:scale-105 transition-transform duration-200"
              draggable="true" @dragstart="drag($event, obj)" @touchstart="(e: TouchEvent) => handleTouchStart(e, obj)"
              @touchmove="(e: TouchEvent) => handleTouchMove(e)" @touchend="handleTouchEnd">

              <div :id="obj.id" class="w-[30px] h-[30px] rounded-full select-none touch-none">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
                <p class="text-white font-bubblegum text-center">{{ obj.weight }}</p>
              </div>

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

      </div>

      <!-- right controls -->
      <div class="flex flex-col justify-center gap-1 absolute right-5 bottom-14 ">
        <button @click="resetGame" class="p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="music" alt="reload" class="w-10 h-10" />
        </button>
        <!-- <button @click="resetGame" class=" p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="more_games" alt="reload" class="w-10 h-10" />
        </button>
        <button @click="resetGame" class=" p-2 text-white sm:left-4 sm:bottom-10 ">
          <img :src="leaderboard" alt="reload" class="w-10 h-10" />
        </button> -->

      </div>

      <LevelComplete v-if="showLevelComplete" :show="showLevelComplete" :message="successMessage"
        :character-src="congratulations_character" @complete="handleLevelComplete"
        class="absolute inset-0 h-full w-full" />

    </template>

  </div>
</template>



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
  flex-direction: column;
  justify-content: center;
  align-items: center;
}


.game-object {
  transition: transform 0.2s ease;
  touch-action: none;
  user-select: none;
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

.game-object.dragging {
  opacity: 0.7;
  transform: scale(1.1);
  pointer-events: none;
  z-index: 1000;
}

.pan.drop-target {
  background-color: rgba(255, 255, 255, 0.2);
  transition: all 0.2s ease;
}

#dragging-clone {
  will-change: transform;
  touch-action: none;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
  image-rendering: -webkit-optimize-contrast;
}
</style>
