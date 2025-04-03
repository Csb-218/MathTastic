<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Activity } from '@/types/activity'
import BalanceScalePreview from '@/components/game_previews/BalanceScalePreview.vue'
import { createActivity, addActivityToGame } from "@/services/GameService"

const route = useRoute()
const router = useRouter()
const gameId = route.params.game_id as string

const newActivity = ref<Activity>({
  addends: [],
  addends_size: 0,
  level: 0,
  hints: [],
  failure_feedback: "",
  success_feedback: "",
  points: 5,
  target: 2,
  time_limit: 0
})

// Watch addends_size changes to update addends array
watch(() => newActivity.value.addends_size, (newSize) => {
  const currentAddends = [...newActivity.value.addends]
  if (newSize > currentAddends.length) {
    // Add new addends
    while (currentAddends.length < newSize) {
      currentAddends.push(0)
    }
  } else {
    // Remove excess addends
    while (currentAddends.length > newSize) {
      currentAddends.pop()
    }
  }
  newActivity.value.addends = currentAddends
})

const isValid = computed(() => {
  return newActivity.value.level > 0 &&
    newActivity.value.target > 0 &&
    newActivity.value.target % 2 === 0 && // Ensure target is even
    newActivity.value.addends_size >= 2 &&
    newActivity.value.addends.every(num => num > 0) // All addends must be positive
})

const updateGame = async () => {
  if (!isValid.value) return

  console.log(newActivity.value)

  try {
    const activity = await createActivity(newActivity.value)


  } catch (error) {
    console.error("Error creating activity:", error)
  }

}
</script>

<template>
  <div class="container mx-auto px-4 py-8 my-4">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bubblegum text-gray-800">Create Balance Game Activity</h1>
      <button @click="router.back()" class="text-gray-600 hover:text-gray-800">
        ← Back
      </button>
    </div>

    <!-- Updated grid layout with specific width distribution -->
    <div class="flex gap-8">
      <!-- Form section - 40% width -->
      <div class="w-[40%]">
        <form @submit.prevent="updateGame" class="bg-white rounded-xl shadow-lg p-6 space-y-6">
          <div class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Basic Settings</h2>
            <div>
              <label class="block text-sm font-medium text-gray-700">Level</label>
              <input type="number" v-model="newActivity.level" min="1"
                class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Target Number (Even Only)</label>
              <input type="number" v-model="newActivity.target" :step="2" min="2"
                @input="e => { const target = e.target as HTMLInputElement; if (target) newActivity.target = Math.floor(+target.value / 2) * 2 }"
                class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">
                Number of Addends: {{ newActivity.addends_size }}
              </label>
              <input type="range" v-model="newActivity.addends_size" min="2" max="10"
                class="mt-2 w-full h-2 bg-amber-200 rounded-lg appearance-none cursor-pointer ">
            </div>

            <div class="space-y-3">
              <h3 class="text-sm font-medium text-gray-700">Addend Values</h3>
              <div class="grid grid-cols-2 gap-4">
                <div v-for="(_, index) in newActivity.addends" :key="index">
                  <label class="block text-xs text-gray-500">Number {{ index + 1 }}</label>
                  <input type="number" v-model="newActivity.addends[index]" min="1"
                    class="mt-1 block rounded-md border-amber-300 text-sm outline-amber-300 border-[0.5px] w-1/5 p-1">
                </div>
              </div>
            </div>
          </div>


          <div class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Feedback Messages</h2>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Success Message</label>
                <input type="text" v-model="newActivity.success_feedback"
                  class="mt-1 block w-full rounded-md border-green-300 outline-green-600 border-[0.5px] p-1">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Failure Message</label>
                <input type="text" v-model="newActivity.failure_feedback"
                  class="mt-1 block w-full rounded-md border-red-300 outline-red-600 border-[0.5px] p-1">
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button type="submit" :disabled="!isValid"
              class="w-full bg-amber-500 text-white px-6 py-3 rounded-full hover:bg-amber-600 disabled:opacity-50">
              Create Activity
            </button>
            <p v-if="!isValid" class="mt-2 text-sm text-red-500">
              Please ensure all fields are filled correctly and target number is even
            </p>
          </div>
        </form>
      </div>

      <!-- Preview section - 60% width -->
      <div class="flex-1">
        <div class="bg-white rounded-xl shadow-lg p-6 h-full">
          <h2 class="text-xl font-semibold text-gray-800 mb-4">Game Preview</h2>
          <BalanceScalePreview :activity="newActivity" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom slider styling */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #f59e0b;
  border-radius: 50%;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #f59e0b;
  border-radius: 50%;
  cursor: pointer;
}
</style>
