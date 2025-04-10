<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Activity } from '@/types/activity'
import type { Game } from '@/types/game'
import { Button } from "@/components/ui/button"
import { useToast } from '@/components/ui/toast/use-toast'
import { Toaster } from '@/components/ui/toast'
import BalanceScalePreview from '@/components/game_previews/BalanceScalePreview.vue'
import AlertDialogDelete from "@/components/blocks/Overlays/AlertDelete.vue"
import { createActivity, addActivityToGame, getGameById, deleteActivity, removeActivityFromGame } from "@/services/GameService"


const route = useRoute()
const router = useRouter()
const gameId = route.params.game_id as string

const { toast } = useToast()
const selectedActivity = ref<Activity | null>(null)
const gameActivities = ref<Activity[]>([])

const newActivity = ref<Activity>({
  _id: "",
  addends: [],
  addends_size: 0,
  level: 0,
  hints: [],
  failure_feedback: "",
  success_feedback: "",
  points: 5,
  target: 20,
  time_limit: 0
})

const enforceEvenTarget = (event: Event) => {
  const value = Number((event.target as HTMLInputElement).value);
  if (value % 2 !== 0) {
    newActivity.value.target = Math.floor(value / 2) * 2;
  }
};

const isValid = computed(() => {
  // Basic field validation
  if (!newActivity.value.level || newActivity.value.level <= 0) return false;

  if (!newActivity.value.target || newActivity.value.target <= 0 || newActivity.value.target % 2 !== 0) return false; // Added even number check

  if (!newActivity.value.addends_size || newActivity.value.addends_size < 2) return false;

  if (!newActivity.value.points || newActivity.value.points < 1 || newActivity.value.points > 100) return false;

  // Addends validation
  if (
    !newActivity.value.addends.length ||                           // Check if addends array exists
    newActivity.value.addends.length !== Number(newActivity.value.addends_size) || // Check length matches size
    newActivity.value.addends.some(num => !num || num <= 0)       // Check all numbers are positive and non-zero
  ) {
    return false;
  }


  // Feedback messages validation
  if (!newActivity.value.success_feedback?.trim() ||
    !newActivity.value.failure_feedback?.trim()) {
    return false;
  }


  // Sum of addends should equal target
  const addendsSum = newActivity.value.addends.reduce((sum, num) => sum + num, 0);
  if (addendsSum !== newActivity.value.target) {
    return false;
  }


  return true;
})

const addHint = () => {
  newActivity.value.hints.push('');
};

const removeHint = (index: number) => {
  newActivity.value.hints.splice(index, 1);
};

const handleSelectActivity = (activity: Activity) => {

  // Check if the selected activity is already selected
  if (selectedActivity.value?._id === activity._id) {
    // If it is, deselect it
    selectedActivity.value = null
    newActivity.value = {
      _id: "",
      addends: [],
      addends_size: 0,
      level: gameActivities.value.length + 1,
      hints: [],
      failure_feedback: "",
      success_feedback: "",
      points: 5,
      target: 2,
      time_limit: 0
    }
    return
  }
  selectedActivity.value = activity
  newActivity.value = {
    ...activity,
    level: gameActivities.value.length + 1,
    addends: [...activity.addends],  // Create a new array with the same values
    hints: [...activity.hints]       // Create a new array for hints as well
  }

  newActivity.value.addends_size = newActivity.value.addends.length

}

const handleDeleteActivity = async () => {
  if (!selectedActivity.value) return

  try {
    await deleteActivity(selectedActivity.value._id)
    await removeActivityFromGame(gameId, selectedActivity.value._id)
  } catch (error) {
    console.error("Error deleting activity:", error)
  } finally {
    toast({
      title: 'Deleted',
      description: 'Activity deleted successfully.',
      duration: 2000,
      variant: "default"
    });
    selectedActivity.value = null
    fetchGameActivities()
  }
}

const updateGame = async () => {
  if (!isValid.value) return

  try {

    const activity = await createActivity(newActivity.value)
    await addActivityToGame(gameId, activity.id)

  } catch (error) {
    console.error("Error creating activity:", error)
  } finally {
    // Reset the form after successful creation
    newActivity.value = {
      _id: "",
      addends: [],
      addends_size: 0,
      level: gameActivities.value.length + 1,
      hints: [],
      failure_feedback: "",
      success_feedback: "",
      points: 5,
      target: 2,
      time_limit: 0
    }

    selectedActivity.value = null

    toast({
      title: 'Activity Created',
      description: 'Added activity successfully.',
      duration: 2000,
      variant: "default"
    });

    fetchGameActivities()

  }

}

const fetchGameActivities = async () => {
  try {
    const game: Game = await getGameById(gameId)
    gameActivities.value = game.activities
    newActivity.value.level = gameActivities.value.length + 1
  } catch (error) {
    console.error("Error fetching game data:", error)
  }
}

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


onMounted(() => fetchGameActivities())


</script>

<template>
  <div class="container mx-auto px-4 py-8 my-4">
    <Toaster class="border-green-400" />

    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bubblegum text-gray-800">Create Balance Game Activity</h1>
      <button @click="router.back()" class="text-gray-600 hover:text-gray-800">
        ← Back
      </button>
    </div>
    <!-- levels -->
    <div class="flex gap-4 mb-8">
      <div v-for="activity in gameActivities" :key="activity._id">
        <Button :variant="`${activity._id !== selectedActivity?._id ? 'outline' : 'default'}`"
          :onclick="() => handleSelectActivity(activity)">Level {{ activity.level }}</Button>
      </div>

    </div>

    <!-- Updated grid layout with specific width distribution -->
    <div class="flex lg:gap-8 lg:flex-row flex-col gap-4">
      <!-- Form section - 40% width -->
      <div class="lg:w-[40%]">
        <form @submit.prevent="updateGame" class="bg-white rounded-xl shadow-lg p-6 space-y-6 relative">
          <!-- delete dialog button -->
          <AlertDialogDelete :selectedActivity="selectedActivity" :handleDeleteActivity="handleDeleteActivity" />

          <div class="space-y-4">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Basic Settings</h2>
            <div>
              <label class="block text-sm font-medium text-gray-700">Level</label>
              <input type="number" v-model="newActivity.level" disabled
                class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Target Number (Even Only)</label>
              <input type="number" v-model="newActivity.target" :step="2" min="2"
                class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block"
                @input="enforceEvenTarget">
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

          <div>
            <label class="block text-sm font-medium text-gray-700">Points</label>
            <input type="number" v-model="newActivity.points" min="1" max="100"
              class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
          </div>

          <div class="space-y-3">
            <h3 class="text-sm font-medium text-gray-700">Hints</h3>
            <div class="space-y-2">
              <div v-for="(hint, index) in newActivity.hints" :key="index" class="flex gap-2">
                <input type="text" v-model="newActivity.hints[index]"
                  class="mt-1 block w-full rounded-md border-amber-300 outline-amber-300 border-[0.5px] p-1"
                  :placeholder="`Hint ${index + 1}`">
                <button type="button" @click="removeHint(index)" class="text-red-500 hover:text-red-700">
                  ✕
                </button>
              </div>
              <button type="button" @click="addHint"
                class="mt-2 px-4 py-1 text-sm bg-amber-100 text-amber-700 rounded-md hover:bg-amber-200">
                Add Hint
              </button>
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
              {{ isValid ? '' : 'Please fill in all required fields correctly.' }}
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
