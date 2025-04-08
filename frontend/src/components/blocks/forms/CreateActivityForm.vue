<template>
  <form @submit.prevent="updateGame" class="bg-white rounded-xl shadow-lg p-6 space-y-6 relative">
    <!-- Add delete button at top right -->
    <Button type="button" variant="ghost" size="icon" @click="handleDeleteActivity(localActivity._id)"
      class="absolute top-4 right-4 hover:bg-red-100 hover:text-red-600" title="Delete Activity">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
        <path d="M3 6h18" />
        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
        <line x1="10" y1="11" x2="10" y2="17" />
        <line x1="14" y1="11" x2="14" y2="17" />
      </svg>
    </Button>

    <div class="space-y-4">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Basic Settings</h2>

      <div>
        <label class="block text-sm font-medium text-gray-700">Level</label>
        <input type="number" v-model="localActivity.level" readonly disabled
          class="mt-1 p-1 rounded-md bg-gray-50 border-gray-300 outline-none border-[0.5px] w-1/5 block cursor-not-allowed">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Target Number (Even Only)</label>
        <input type="number" v-model="localActivity.target" :step="2" min="2"
          class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">
          Number of Addends: {{ localActivity.addends_size }}
        </label>
        <input type="range" v-model="localActivity.addends_size" min="2" max="10"
          class="mt-2 w-full h-2 bg-amber-200 rounded-lg appearance-none cursor-pointer ">
      </div>

      <div class="space-y-3">
        <h3 class="text-sm font-medium text-gray-700">Addend Values</h3>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="(value, index) in localActivity.addends" :key="index">
            <label class="block text-xs text-gray-500">Number {{ index + 1 }}</label>
            <input type="number" v-model.number="localActivity.addends[index]" min="1"
              class="mt-1 block rounded-md border-amber-300 text-sm outline-amber-300 border-[0.5px] w-1/5 p-1">
          </div>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Points</label>
        <input type="number" v-model="localActivity.points" min="1" max="100"
          class="mt-1 p-1 rounded-md border-amber-300 outline-amber-300 border-[0.5px] w-1/5 block">
      </div>

      <div class="space-y-3">
        <h3 class="text-sm font-medium text-gray-700">Hints</h3>
        <div class="space-y-2">
          <div v-for="(hint, index) in localActivity.hints" :key="index" class="flex gap-2">
            <input type="text" v-model="localActivity.hints[index]"
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
    </div>

    <div class="space-y-4">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Feedback Messages</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Success Message</label>
          <input type="text" v-model="localActivity.success_feedback"
            class="mt-1 block w-full rounded-md border-green-300 outline-green-600 border-[0.5px] p-1">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Failure Message</label>
          <input type="text" v-model="localActivity.failure_feedback"
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
</template>

<script setup lang="ts">
import { reactive, watch, computed } from 'vue';
import type { Activity } from '@/types/activity';
import { Button } from "@/components/ui/button";

const emit = defineEmits(['update:activity']);

const { updateGame, newActivity, handleDeleteActivity } = defineProps<{
  updateGame: () => void;
  newActivity: Activity;
  handleDeleteActivity: (id: string) => void;
}>();

const localActivity = reactive({ ...newActivity });

const addHint = () => {
  const currentAddends = [...localActivity.addends]; // Save current addends
  const currentAddendSize = localActivity.addends_size; // Save current size
  localActivity.hints.push('');
  // Restore addends and size after adding hint
  localActivity.addends = currentAddends;
  localActivity.addends_size = currentAddendSize;
  emit('update:activity', localActivity);
};

const removeHint = (index: number) => {
  const currentAddends = [...localActivity.addends]; // Save current addends
  const currentAddendSize = localActivity.addends_size; // Save current size
  localActivity.hints.splice(index, 1);
  // Restore addends and size after removing hint
  localActivity.addends = currentAddends;
  localActivity.addends_size = currentAddendSize;
  emit('update:activity', localActivity);
};

// Update watch handler to preserve hints and addends
watch(() => newActivity, (newVal) => {
  const currentHints = [...localActivity.hints];
  const currentAddends = [...localActivity.addends];
  const currentAddendSize = localActivity.addends_size;

  Object.assign(localActivity, newVal);

  // Restore preserved values
  localActivity.hints = currentHints;
  localActivity.addends = currentAddends;
  localActivity.addends_size = currentAddendSize;
}, { deep: true });

watch(() => localActivity.addends_size, (newSize) => {
  // Convert newSize to number and ensure it's within bounds
  const size = Number(newSize);
  if (size < 2 || size > 10) return;

  // Create a new array with the current values or zeros
  const newAddends = Array(size).fill(0).map((_, index) =>
    localActivity.addends[index] || 0
  );

  // Update the addends array
  localActivity.addends = newAddends;
}, { immediate: true });

// Optional: Watch addends array for changes to ensure size consistency
watch(() => localActivity.addends, (newAddends) => {
  if (newAddends.length !== localActivity.addends_size) {
    localActivity.addends_size = newAddends.length;
  }
}, { deep: true });

const isValid = computed(() => {
  const activity = localActivity;

  // Basic field validation
  if (!activity.level || activity.level <= 0) return false;
  if (!activity.target || activity.target <= 0 || activity.target % 2 !== 0) return false;
  if (!activity.addends_size || activity.addends_size < 2) return false;
  if (!activity.points || activity.points < 1 || activity.points > 100) return false;

  // Addends validation
  if (!activity.addends.length ||
    activity.addends.length !== activity.addends_size ||
    activity.addends.some(num => num <= 0)) {
    return false;
  }

  // Feedback messages validation
  if (!activity.success_feedback?.trim() ||
    !activity.failure_feedback?.trim()) {
    return false;
  }

  // Sum of addends should equal target
  const addendsSum = activity.addends.reduce((sum, num) => sum + num, 0);
  if (addendsSum !== activity.target) {
    return false;
  }

  return true;
});
</script>
