<script setup lang="ts">
import { watch } from 'vue'

// components
import { Button } from '@/components/ui/button'
import NavbarStandard from '@/components/blocks/navigation/NavbarStandard.vue'
import AuthenticationForm from '@/components/blocks/authentication/AuthForm.vue'

import { useAuthPageStore } from "@/stores/Authentication/authPageStore"
const authPageStore = useAuthPageStore()


watch(
  () => authPageStore.student,
  (newValue) => {
    console.log('isStudent changed:', newValue)
  }
)


</script>

<template>

  <div
    class="min-h-screen bg-gradient-to-b from-amber-50 to-white flex flex-col items-center justify-center gap-y-2 px-4">
    <NavbarStandard />

    <!-- Role Selector -->
    <div class="flex gap-2 p-1 bg-gray-100 rounded-lg mb-6">
      <Button :disabled="authPageStore.emailLoading || authPageStore.googleLoading"
        @click="authPageStore.setStudent(true)" :variant="authPageStore.isStudent ? 'default' : 'ghost'">
        Student
      </Button>
      <Button :class="!authPageStore.isStudent && 'bg-blue-500 text-white hover:bg-blue-400'"
        :disabled="authPageStore.emailLoading || authPageStore.googleLoading" @click="authPageStore.setStudent(false)"
        :variant="!authPageStore.isStudent ? 'default' : 'ghost'">
        Educator
      </Button>
    </div>

    <!-- Render appropriate form based on role -->
    <AuthenticationForm />

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
