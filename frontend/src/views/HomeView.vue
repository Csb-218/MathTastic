<script setup lang="ts">
import Hero from "@/components/blocks/Hero/Hero.vue"
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue'
import Footer from "../components/blocks/Footer.vue"
import Games from "../components/blocks/Hero/GamesSection.vue"
import FAQ from '@/components/blocks/Hero/FAQ.vue'
import Testimonials from '../components/blocks/Hero/Testimonials.vue'
import ChildPlay from "@/assets/childplay.svg"
import type { Game } from '@/types/game'


const dummyGames: Game[] = [
  {
    id: "1",
    title: "Balance the Scale",
    description: "Learn addition and subtraction by balancing weights on a scale",
    image: "https://scoonews.com/wp-content/uploads/2022/07/cover15851292261585129226.jpg",
    difficulty: "easy",
    age_range: "6-8",
    activities: [], // Initialize as empty array
    target_range: [1, 20],
    total_points: 100,
    template: false
  },
  {
    id: '2',
    title: "Number Ninja",
    description: "Slice through numbers to master multiplication tables",
    image: "https://store-images.s-microsoft.com/image/apps.65264.13510798882430817.b10ab5df-3d92-47ad-9d56-96b15f73d63f.f3743b21-d1d9-4f19-9f7f-042b30214eef?mode=scale&q=90&h=1080&w=1920",
    difficulty: "medium",
    age_range: "8-10",
    activities: [],
    target_range: [1, 50],
    total_points: 150,
    template: false
  },
  {
    id: '3',
    title: "Fraction Factory",
    description: "Build and compare fractions in this fun factory game",
    image: "https://storage.googleapis.com/ltkcms.appspot.com/fs/wfa/images/cover/wordsmith.base?v=1599144875",
    difficulty: "hard",
    age_range: "9-11",
    activities: [],
    target_range: [1, 100],
    total_points: 200,
    template: false
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
          <Games :games="dummyGames" />
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
  <Footer />
</template>
