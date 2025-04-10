<template>
  <span>{{ displayText }}</span>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  text: string;
  delay?: number;
}>();

const displayText = ref('');

const typeText = async () => {
  displayText.value = '';
  for (let i = 0; i < props.text.length; i++) {
    await new Promise(resolve => setTimeout(resolve, props.delay || 50));
    displayText.value += props.text[i];
  }
};

watch(() => props.text, typeText, { immediate: true });
</script>
