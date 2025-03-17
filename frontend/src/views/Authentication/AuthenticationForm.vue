<script setup lang="ts">
import { ref } from 'vue'

// components
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue'
import StudentForm from '@/components/blocks/authentication/StudentForm.vue'
import EducatorForm from '@/components/blocks/authentication/EducatorForm.vue'


const userRole = ref('student')

</script>

<template>

  <div
    class="min-h-screen bg-gradient-to-b from-amber-50 to-white flex flex-col items-center justify-center gap-y-2 px-4">
    <NavbarStandard />

    <!-- Role Selector -->
    <div class="flex gap-2 p-1 bg-gray-100 rounded-lg mb-6">
      <button v-for="role in ['student', 'educator']" :key="role" @click="userRole = role" :class="[
        'flex-1 py-2 px-4 rounded-md transition-colors',
        userRole === role
          ? 'bg-amber-500 text-white shadow'
          : 'text-gray-600 hover:bg-gray-200'
      ]">
        {{ role.charAt(0).toUpperCase() + role.slice(1) }}
      </button>
    </div>

    <!-- Render appropriate form based on role -->
    <StudentForm v-if="userRole === 'student'" />
    <EducatorForm v-if="userRole === 'educator'" />

  </div>
</template>

<style scoped>
.text-red-600 {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>
