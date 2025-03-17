<script setup lang="ts">
const testimonials = [
  {
    id: 1,
    quote: "My 6-year-old begs to play! She's adding numbers faster than I can check!",
    author: "Sarah M.",
    role: "Mom of 2",
    location: "Seattle, WA",
    image: "https://randomuser.me/api/portraits/women/1.jpg"
  },
  {
    id: 2,
    quote: "I love making the scale balance! The cookies jump when I get it right!",
    author: "Liam K.",
    role: "Student",
    age: "7 years old",
    image: "https://randomuser.me/api/portraits/kids/1.jpg"
  },
  {
    id: 3,
    quote: "Perfect for differentiated learning. I assign levels based on each student's needs.",
    author: "Mr. Davis",
    role: "3rd Grade Teacher",
    location: "Chicago, IL",
    image: "https://randomuser.me/api/portraits/men/1.jpg"
  },
  {
    id: 4,
    quote: "The progress tracking helps me understand exactly where my child needs support.",
    author: "Emily R.",
    role: "Parent",
    location: "Boston, MA",
    image: "https://randomuser.me/api/portraits/women/2.jpg"
  },
  {
    id: 5,
    quote: "The game-based approach makes math practice fun and engaging for my students!",
    author: "Ms. Thompson",
    role: "Math Specialist",
    location: "Austin, TX",
    image: "https://randomuser.me/api/portraits/women/3.jpg"
  }
]
</script>

<template>
  <section class="py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-8 text-gray-900">What Our Users Say</h2>
      
      <div class="relative">
        <!-- Scrollable container -->
        <div class="flex overflow-x-auto gap-6 pb-8 snap-x snap-mandatory scrollbar-hide">
          <!-- Individual testimonials -->
          <div 
            v-for="testimonial in testimonials" 
            :key="testimonial.id"
            class="flex-none w-80 md:w-96 snap-center"
          >
            <div class="bg-white p-6 rounded-xl shadow-lg">
              <!-- Quote -->
              <div class="mb-6">
                <svg class="h-8 w-8 text-amber-400 mb-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.999v10h-9.999z"/>
                </svg>
                <p class="text-gray-600 italic">{{ testimonial.quote }}</p>
              </div>
              
              <!-- Author -->
              <div class="flex items-center">
                <img 
                  :src="testimonial.image" 
                  :alt="testimonial.author"
                  class="h-12 w-12 rounded-full object-cover"
                >
                <div class="ml-4">
                  <h4 class="font-semibold text-gray-900">{{ testimonial.author }}</h4>
                  <p class="text-sm text-gray-500">{{ testimonial.role }}</p>
                  <p v-if="testimonial.location" class="text-sm text-gray-500">{{ testimonial.location }}</p>
                  <p v-if="testimonial.age" class="text-sm text-gray-500">{{ testimonial.age }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Scroll indicators -->
        <div class="flex justify-center mt-4 gap-2">
          <div v-for="n in 5" :key="n" class="h-2 w-2 rounded-full bg-gray-300"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Hide scrollbar but keep functionality */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>