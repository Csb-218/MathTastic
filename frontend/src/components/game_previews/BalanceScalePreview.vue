<template>

  <div ref="gameContainer"
    class="game-container  bg-[url(@/assets/backgrounds/rainbow_landscape.jpg)] bg-cover text-center  bg-[#f5f5d5] font-sans relative aspect-video">

    <div class="relative h-full">
      <!-- Level board -->
      <span class="absolute top-4 left-1/2 -translate-x-1/2 p-2 text-white">
        <img :src="level_board" alt="level_board" class="h-20" />
        <p class="z-50 absolute top-1/3 left-1/2 -translate-x-1/2 font-bubblegum text-2xl ">Level {{ currentLevel }}
        </p>
      </span>



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
            class="pan left-pan absolute top-[40px] -left-11 w-[100px] h-[100px] flex flex-wrap-reverse items-start py-2 justify-center"
            @drop="drop($event, 'left')" @dragover="allowDrop">
            <div v-for="obj in leftPanObjects" :key="obj.id" class="object-container">
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " draggable="true"
                @dragstart="drag($event, obj)">
                <img v-if="obj.image" :src="obj.image" :alt="obj.type" class="w-full h-full object-contain" />
              </div>
            </div>
            <p class="absolute -bottom-7 font-bubblegum text-white text-lg">{{ leftWeight }}</p>
          </div>
          <div
            class="pan right-pan absolute top-[40px] -right-11 w-[100px] h-[100px] flex flex-wrap-reverse items-start py-2 justify-center"
            @drop="drop($event, 'right')" @dragover="allowDrop">
            <div v-for="obj in rightPanObjects" :key="obj.id" class="object-container">
              <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " draggable="true"
                @dragstart="drag($event, obj)">
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
            <div :id="obj.id" class="game-object w-[30px] h-[30px] rounded-full " draggable="true"
              @dragstart="drag($event, obj)">
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

      <LevelComplete v-if="showMessage" :show="showMessage" :message="activity.success_feedback"
        :character-src="congratulations_character" @complete="handleLevelComplete"
        class="absolute inset-0 h-full w-full" />
    </div>

  </div>

</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useEventListener } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import type { Activity } from '@/types/activity'
import { createWeighingObjectsFromActivity } from '@/lib/helpers'
//store
import { useBalanceScaleStore } from '@/stores/Gameplay/BalanceScale/balanceScale'
// assets
import { leaderboard, level_board, more_games, music, nut, reload, stand } from "@/assets/game"
import LevelComplete from '@/components/blocks/game/LevelComplete.vue';
import { congratulations_character } from '@/assets/game'




// props
const { activity } = defineProps<{
  activity: Activity
}>()

// States
const currentLevel = ref<number>(0)
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
  isFullScreen } = storeToRefs(useBalanceScaleStore())

const {
  initGameObjects,
  fullScreenChange,
  exitGame,
  drop,
  drag,
  allowDrop,
  resetGame
} = useBalanceScaleStore()




// Methods

// resize
const handleResize = () => {
  isMobileView.value = window.innerWidth < 768
}

// Fetch game state
const fetchGameState = () => {
  try {
    loading.value = true
    const activity_objects = createWeighingObjectsFromActivity(activity)
    initGameObjects(activity_objects)
    currentLevel.value = activity.level
  } catch (err) {
    error.value = 'Failed to load game objects'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Add watch for activity changes
watch(
  () => activity,
  async (newActivity) => {
    if (newActivity) {
      fetchGameState()
    }
  },
  { deep: true }
)

const handleLevelComplete = async () => {
  setTimeout(() => {
    showMessage.value = false
  }, 3000)
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
}

.game-object:hover {
  transform: scale(1.1);
}

.loading-spinner {
  @apply text-amber-600 text-xl font-bold;
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
