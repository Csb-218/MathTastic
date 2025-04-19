<template>
  <div class="min-h-screen backdrop-blur-xs p-6">
    <!-- Page Title -->
    <p class="text-3xl font-bubblegum text-left text-blue-500  animated-glow  mb-6">Dashboard</p>

    <!-- Grid Layout for Sections -->


    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <ErrorBoundary>
        <!-- Profile Card -->
        <div class="bg-white p-6 rounded-lg shadow-md ">
          <div class="flex flex-wrap items-center gap-x-3.5 ">
            <img :src="profile.picture" alt="Profile Picture"
              class="w-24 h-24 rounded-sm mr-4 object-cover p-2 border-2 border-amber-400" />
            <div class="w-7/12 ">
              <p class="text-4xl font-bubblegum">{{ profile.name }}</p>
              <p class="text-gray-600 text-2xl font-bubblegum">{{ profile.age }} years old</p>
              <p class="text-gray-600 text-2xl font-bubblegum">Grade {{ profile.grade }}</p>
            </div>
            <div>
              <div class="relative">
                <img class="w-24 h-24" :src="star" alt="info_orange" />
                <p class="text-white text-xl absolute font-bubblegum top-10 left-1/3 ">1200</p>
              </div>
              <p class="font-bubblegum ">Points earned </p>
            </div>
          </div>
        </div>
      </ErrorBoundary>

      <!-- View more Card -->
      <div class="bg-gray-100 p-4 rounded-lg shadow-md font-bubblegum grid grid-cols-1 gap-1">
        <!-- Header -->
        <div class="flex justify-between items-center mb-2">
          <div class="flex items-center">
            <h2 class="text-lg font-semibold text-blue-600">Suggested Skill</h2>
            <svg class="w-5 h-5 ml-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
              </path>
            </svg>
          </div>
          <a href="#" class="text-blue-600 text-sm hover:underline">
            View More
            <span class="ml-1">&raquo;</span>
          </a>
        </div>

        <!-- No Assigned Work Section -->
        <div class="bg-cyan-500 text-white p-4 rounded-lg mb-2 flex items-center ">
          <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0113.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m0-16l1.761.94c.159.04.322.06.485.06H13.263a2 2 0 011.789 1.106l3.5 7A2 2 0 0118.764 14H14m-7 0h4">
            </path>
          </svg>
          <div>
            <p class="text-lg font-semibold">No assigned work!</p>
            <p class="text-sm">Try one of our suggested games below</p>
          </div>
        </div>

        <!-- Free Play Section -->
        <div class="bg-yellow-400 text-black p-4 rounded-lg flex items-center justify-between">
          <p class="text-lg font-semibold">Free Play</p>
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4m4-4v8m8-8v8"></path>
          </svg>
        </div>
      </div>

      <!-- Latest Progress -->
      <div class="bg-white font-bubblegum text-2xl p-6 rounded-lg shadow-md col-span-1 md:col-span-2 overflow-scroll">
        <p class=" mb-4">Latest Progress</p>
        <table class="table-auto w-full text-left border-collapse ">
          <thead>
            <tr class="bg-cyan-100">
              <th class=" px-4 py-2">Skill</th>
              <th class=" px-4 py-2">Level</th>
              <th class=" px-4 py-2">Attempted</th>
              <th class=" px-4 py-2">Correct</th>
              <th class=" px-4 py-2">Time</th>
              <th class=" px-4 py-2">Last Played</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(skill, index) in skillData" :key="index" class="hover:bg-gray-50">
              <td class=" px-4 py-2">{{ skill.name }}</td>
              <td class=" px-4 py-2">{{ skill.level }}</td>
              <td class=" px-4 py-2">{{ skill.attempted }}</td>
              <td class=" px-4 py-2">{{ skill.correct }}</td>
              <td class=" px-4 py-2">{{ skill.time }}</td>
              <td class=" px-4 py-2">{{ skill.lastPlayed }}</td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>

    <!-- Modal for Editing Profile -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-md w-96">
        <h2 class="text-2xl font-semibold mb-4">Edit Profile</h2>
        <form @submit.prevent="saveProfile">
          <div class="mb-4">
            <label class="block text-gray-700">Name</label>
            <input v-model="profile.name" class="w-full p-2 border rounded" type="text" />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Age</label>
            <input v-model="profile.age" class="w-full p-2 border rounded" type="number" />
          </div>
          <div class="mb-4">
            <label class="block text-gray-700">Grade</label>
            <input v-model="profile.grade" class="w-full p-2 border rounded" type="number" />
          </div>
          <div class="flex justify-end">
            <button @click="showModal = false" class="bg-gray-500 text-white px-4 py-2 rounded mr-2">
              Cancel
            </button>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
// import info_orange from "@/assets/icons/Info_orange.png"
import star from "@/assets/icons/star.svg"
import ErrorBoundary from '@/components/blocks/ErrorBoundary.vue';
import { useAuthStore } from "@/stores/Authentication/authStore"

const authStore = useAuthStore()
// Profile Data
const profile = ref({
  name: authStore.get_user.name,
  age: 10,
  grade: 5,
  picture: authStore.get_user.picture || "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR54iRKN5gGKCLLrjfUveGRhmhjv4r219tmqQ&s",
});

const skillData = ref({
  Math: { name: '2.1 Geometry of Everyday Objects', level: 3, attempted: 10, correct: 8, time: '10 mins', lastPlayed: '2023-03-10' },
  Science: { name: '4.1 Area with Unit Squares and Units', level: 2, attempted: 5, correct: 3, time: '5 mins', lastPlayed: '2023-02-15' },
});


// Modal State
const showModal = ref(false);

// Save Profile Function
const saveProfile = () => {
  // In a real app, this would update the data on a server
  showModal.value = false;
};
</script>

<style scoped>
.glow {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.7),
    0 0 20px rgba(255, 255, 255, 0.7);
}

/* Amber glow for your student profile */
.amber-glow {
  text-shadow: 0 0 10px rgba(251, 191, 36, 0.7),
    0 0 20px rgba(251, 191, 36, 0.7);
}

/* Cyan glow for your table headers */
.cyan-glow {
  text-shadow: 0 0 10px rgba(6, 182, 212, 0.7),
    0 0 20px rgba(6, 182, 212, 0.7);
}

/* Animated glow effect */
.animated-glow {
  animation: glowing 2s ease-in-out infinite;
}

@keyframes glowing {

  0%,
  100% {
    text-shadow: 0 0 10px rgba(251, 191, 36, 0.7),
      0 0 20px rgba(251, 191, 36, 0.7);
  }

  50% {
    text-shadow: 0 0 20px rgba(251, 191, 36, 0.9),
      0 0 30px rgba(251, 191, 36, 0.9);
  }
}
</style>
