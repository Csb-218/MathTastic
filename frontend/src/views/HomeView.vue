<script setup lang="ts">
import Hero from "@/components/blocks/Hero/Hero.vue"
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue'
import Footer from "../components/blocks/Footer.vue"
import Games from "../components/blocks/Hero/Games.vue"
import FAQ from '@/components/blocks/Hero/FAQ.vue'
import Testimonials from '../components/blocks/Hero/Testimonials.vue'
import ChildPlay from "@/assets/childplay.svg"

const gamesList = [
  {
    id: 1,
    title: "Balance Fun",
    description: "Learn addition by balancing numbers on a magical scale!",
    image: "https://picsum.photos/id/101/800/600",
    level: "Beginner",
    ageRange: "4-6 years"
  },
  {
    id: 2,
    title: "Number Quest",
    description: "Embark on an adventure to find matching number pairs!",
    image: "https://picsum.photos/id/102/800/600",
    level: "Intermediate",
    ageRange: "6-8 years"
  },
  {
    id: 3,
    title: "Math Heroes",
    description: "Save the day by solving exciting math challenges!",
    image: "https://picsum.photos/id/103/800/600",
    level: "Advanced",
    ageRange: "8-10 years"
  },
  {
    id: 4,
    title: "Balance Fun",
    description: "Learn addition by balancing numbers on a magical scale!",
    image: "https://picsum.photos/id/101/800/600",
    level: "Beginner",
    ageRange: "4-6 years"
  },
  {
    id: 5,
    title: "Number Quest",
    description: "Embark on an adventure to find matching number pairs!",
    image: "https://picsum.photos/id/102/800/600",
    level: "Intermediate",
    ageRange: "6-8 years"
  },
  {
    id: 6,
    title: "Math Heroes",
    description: "Save the day by solving exciting math challenges!",
    image: "https://picsum.photos/id/103/800/600",
    level: "Advanced",
    ageRange: "8-10 years"
  }
]

</script>

<template>
  <!-- Responsive Navbar -->
  <NavbarStandard />
  <div class="min-h-screen mt-16 bg-gradient-to-r to-amber-200 from-cyan-100">
    <!-- Main Content with padding for fixed navbar -->
    <main class="pt-20 flex flex-col items-center">
      <!-- Hero Section -->
      <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-16  ">
        <Hero />
      </section>

      <!-- Features Grid of Games -->
      <section class=" bg-white py-12 sm:py-16">
        <div class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-12">
          <Games :games="gamesList" />
        </div>
      </section>

      <!-- FAQs -->
      <section class="  py-12 sm:py-16">
        <div class=" flex gap-2 max-w-8xl mx-auto px-4 sm:px-6 lg:px-8">
          <FAQ />
          <img :src="ChildPlay" class="w-5/12">
        </div>
      </section>

      <section class="bg-white  py-12 sm:py-16">
        <div class=" max-w-screen lg:w-full mx-auto px-4 sm:px-6 lg:px-12">
          <Testimonials />
        </div>
      </section>
    </main>

  </div>
  <Footer/>
</template>
