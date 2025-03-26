<script setup lang="ts">
import { ref } from 'vue'
import type { Game } from '@/types/game'
import type { Activity } from '@/types/activity'

// Form data
const gameData = ref<Partial<Game>>({
  title: '',
  description: '',
  activities: [],
  image: '',
  level: '',
  ageRange: '',
  targetRange: [0, 0],
  totalPoints: 0,
  template: false
})

const currentActivity = ref<Partial<Activity>>({
  level: 1,
  target: 0,
  addends: [],
  addends_size: 2,
  time_limit: 60,
  hints: [],
  points: 10,
  success_feedback: '',
  failure_feedback: ''
})

const currentHint = ref('')

// Methods
const addHint = () => {
  if (currentHint.value.trim()) {
    currentActivity.value.hints?.push(currentHint.value)
    currentHint.value = ''
  }
}

const removeHint = (index: number) => {
  currentActivity.value.hints?.splice(index, 1)
}

const addActivity = () => {
  if (currentActivity.value && isActivityValid()) {
    gameData.value.activities?.push({ ...currentActivity.value } as Activity)
    resetActivityForm()
    updateTotalPoints()
  }
}

const removeActivity = (index: number) => {
  gameData.value.activities?.splice(index, 1)
  updateTotalPoints()
}

const updateTotalPoints = () => {
  gameData.value.totalPoints = gameData.value.activities?.reduce(
    (sum, activity) => sum + activity.points, 0
  ) || 0
}

const isActivityValid = () => {
  return currentActivity.value.target &&
    currentActivity.value.addends?.length &&
    currentActivity.value.hints?.length
}

const resetActivityForm = () => {
  currentActivity.value = {
    level: 1,
    target: 0,
    addends: [],
    addends_size: 2,
    time_limit: 60,
    hints: [],
    points: 10,
    success_feedback: '',
    failure_feedback: ''
  }
}

const handleSubmit = () => {
  // TODO: Add validation and API call
  console.log('Game data:', gameData.value)
}
</script>

<template>
  <div class="max-w-4xl mx-auto p-6 mt-20">
    <h1 class="text-3xl font-bold mb-8">Create New Game</h1>

    <!-- Game Details Form -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Game Details</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Title</label>
          <input v-model="gameData.title" type="text" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Level</label>
          <select v-model="gameData.level" class="w-full p-2 border rounded">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Age Range</label>
          <input v-model="gameData.ageRange" type="text" class="w-full p-2 border rounded" placeholder="e.g., 8-10" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Description</label>
          <textarea v-model="gameData.description" class="w-full p-2 border rounded" rows="3"></textarea>
        </div>
      </div>
    </div>

    <!-- Activity Form -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Add Activity</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Target Number</label>
          <input v-model="currentActivity.target" type="number" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Time Limit (seconds)</label>
          <input v-model="currentActivity.time_limit" type="number" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Points</label>
          <input v-model="currentActivity.points" type="number" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Number of Addends</label>
          <input v-model="currentActivity.addends_size" type="number" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Success Feedback</label>
          <input v-model="currentActivity.success_feedback" type="text" class="w-full p-2 border rounded" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">Failure Feedback</label>
          <input v-model="currentActivity.failure_feedback" type="text" class="w-full p-2 border rounded" />
        </div>
      </div>

      <!-- Hints Section -->
      <div class="mt-4">
        <label class="block text-sm font-medium mb-1">Hints</label>
        <div class="flex gap-2 mb-2">
          <input v-model="currentHint" type="text" class="flex-1 p-2 border rounded" placeholder="Add a hint" />
          <button @click="addHint" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Add Hint
          </button>
        </div>
        <ul v-if="currentActivity.hints?.length" class="space-y-2">
          <li v-for="(hint, index) in currentActivity.hints" :key="index" class="flex items-center gap-2">
            <span>{{ hint }}</span>
            <button @click="removeHint(index)" class="text-red-500 hover:text-red-600">Remove</button>
          </li>
        </ul>
      </div>

      <button @click="addActivity" class="mt-4 px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600">
        Add Activity
      </button>
    </div>

    <!-- Activities List -->
    <div v-if="gameData.activities?.length" class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Activities ({{ gameData.activities.length }})</h2>
      <div class="space-y-4">
        <div v-for="(activity, index) in gameData.activities" :key="index" class="border p-4 rounded">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-medium">Activity {{ index + 1 }}</h3>
              <p>Target: {{ activity.target }} | Points: {{ activity.points }} | Time: {{
                activity.time_limit }}s</p>
              <p>Hints: {{ activity.hints.join(', ') }}</p>
            </div>
            <button @click="removeActivity(index)" class="text-red-500 hover:text-red-600">Remove</button>
          </div>
        </div>
      </div>
      <div class="mt-4 text-right">
        <p class="font-medium">Total Points: {{ gameData.totalPoints }}</p>
      </div>
    </div>

    <!-- Submit Button -->
    <button @click="handleSubmit"
      class="w-full px-6 py-3 bg-amber-500 text-white rounded-lg hover:bg-amber-600 font-medium">
      Create Game
    </button>
  </div>
</template>
