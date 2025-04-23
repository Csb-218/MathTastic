<script setup lang="ts">
import { ref } from 'vue'

const activeIndex = ref<number | null>(null)

const faqs = [
  {
    id: 1,
    question: "What age group is MathTastic suitable for?",
    answer: "MathTastic is designed for children aged 4-10 years. We have different difficulty levels to match your child's learning stage, from basic number recognition to complex addition problems."
  },
  {
    id: 2,
    question: "How does MathTastic ensure my child's safety online?",
    answer: "We are COPPA-compliant and maintain strict privacy standards. We never collect personal information from children, and all content is ad-free. Parent accounts are required for children under 13."
  },
  {
    id: 3,
    question: "Can teachers use MathTastic in their classroom?",
    answer: "Absolutely! We offer special classroom accounts with features like progress tracking, custom assignments, and detailed analytics. Teachers can manage multiple students and align content with curriculum standards."
  },
  {
    id: 4,
    question: "How does the reward system work?",
    answer: "Children earn stars and badges for completing challenges, maintaining streaks, and achieving milestones. These can be used to unlock new characters, themes, and bonus games."
  },
  {
    id: 5,
    question: "Is there a free trial available?",
    answer: "Yes! You can try MathTastic free for 7 days with full access to all premium features. After that, choose between our basic free plan or premium subscription."
  }
]

const toggleFaq = (index: number) => {
  activeIndex.value = activeIndex.value === index ? null : index
}
</script>

<template>
  <section class="py-12 px-4 sm:px-6 lg:px-8 w-full">
    <div class="max-w-3xl mx-auto w-full">
      <h2 class="text-3xl font-bold  py-2 text-gray-900">Know More About MathTastic</h2>

      <div class="space-y-4 w-full mt-8 ">
        <div
          v-for="(faq, index) in faqs"
          :key="faq.id"
          class="w-2xl bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <button
            @click="toggleFaq(index)"
            class="w-full px-6 py-4 text-left focus:outline-none text-gray-900 flex items-center justify-between"
            :class="{ 'bg-amber-400 text-white': activeIndex === index }"
          >
            <h3 class="text-lg font-semibold  pr-4">{{ faq.question }}</h3>
            <span
              class="transform transition-transform duration-200 ease-in-out"
              :class="{ 'rotate-180': activeIndex === index }"
            >
              <svg class="h-6 w-6 text-gray-500 flex-shrink-0" :class="{ 'text-white': activeIndex === index }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </span>
          </button>
          <transition
            name="expand"
            @enter="el => (el as HTMLElement).style.maxHeight = (el as HTMLElement).scrollHeight + 'px'"
            @leave="el => (el as HTMLElement).style.maxHeight = '0px'"
          >
            <div
              v-show="activeIndex === index"
              class="answer-content overflow-hidden"
            >
              <div class="px-6 pb-4">
                <p class="text-gray-600">{{ faq.answer }}</p>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.transform {
  transition: transform 0.2s ease;
}

.answer-content {
  max-height: 0;
  transition: max-height 0.3s cubic-bezier(0, 1, 0, 1);
}

.expand-enter-active {
  transition: all 0.3s cubic-bezier(1, 0, 1, 0);
}

.expand-leave-active {
  transition: all 0.3s cubic-bezier(0, 1, 0, 1);
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
