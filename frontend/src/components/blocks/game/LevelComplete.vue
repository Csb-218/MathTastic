<template>
  <Transition enter-active-class="transition-all duration-500 ease-out" enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100" leave-active-class="transition-all duration-500 ease-in"
    leave-from-class="translate-y-0 opacity-100" leave-to-class="translate-y-full opacity-0">
    <div v-if="show" class="absolute inset-0 flex items-center justify-center bg-black/50 w-full h-full">
      <div class="relative">
        <!-- Speech Bubble -->
        <div class="speech-bubble bg-white p-6 rounded-2xl mb-4 relative">
          <div class="font-bubblegum text-2xl text-center">
            <TypeWriter :text="message" :delay="50" class="text-amber-600" />
          </div>
          <!-- Triangle pointer for speech bubble -->
          <div class="absolute -bottom-4 left-1/2 -translate-x-1/2
                      w-0 h-0 border-l-[15px] border-l-transparent
                      border-t-[20px] border-t-white
                      border-r-[15px] border-r-transparent">
          </div>
        </div>

        <!-- Character -->
        <div class="character-container relative w-48 h-48">
          <img :src="characterSrc" alt="cartoon character" class="w-full h-full object-contain">
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { watchEffect } from 'vue';
import TypeWriter from '@/components/blocks/game/TypeWriter.vue';

const props = defineProps<{
  show: boolean;
  message: string;
  characterSrc: string;
}>();

const emit = defineEmits(['complete']);

// Auto-hide after 3 seconds
watchEffect(() => {
  if (props.show) {
    setTimeout(() => {
      emit('complete');
    }, 3000);
  }
});
</script>

<style scoped>
.speech-bubble {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-width: 300px;
}

.character-container {
  animation: bounceIn 0.5s ease-out;
}

@keyframes bounceIn {
  0% {
    transform: translateY(100%) scale(0.3);
    opacity: 0;
  }

  50% {
    transform: translateY(-20%) scale(1.1);
  }

  70% {
    transform: translateY(10%) scale(0.9);
  }

  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}
</style>
