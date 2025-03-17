<script lang="tsx">
export default{
    name:"Hero"
}
</script>
<template>
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
          <div class="text-center lg:text-left">
            <h2 class="text-4xl sm:text-5xl font-bold font-fredoka text-gray-900 mb-4 sm:mb-6">
              🎮 Balance Fun & Learning!
            </h2>
            <p class="text-lg py-10 sm:text-xl text-gray-600 mb-6 sm:mb-8">
              Where Math Meets Play: Help Kids Master Addition Through Interactive Balance Challenges!
            </p>
            <button class="w-full sm:w-auto group bg-amber-500 hover:bg-amber-600 text-white px-6 sm:px-8 py-3 sm:py-4 rounded-full text-lg font-semibold transition-all transform hover:scale-105 cursor-pointer">
              👉 Start Learning Free!
              <span class="inline-block transition-transform group-hover:translate-x-2 ml-2">→</span>
            </button>
          </div>
          <div class="relative mt-8 lg:mt-0">
            <div class="aspect-w-4 aspect-h-3  rounded-2xl  ">
              <!-- Placeholder for animation -->
               <img src="https://marketplace.canva.com/-BaQE/MAF_dW-BaQE/1/tl/canva-MAF_dW-BaQE.png" alt="Kids" class="w-full h-full object-cover ">

            </div>
          </div>
        </div>
</template>