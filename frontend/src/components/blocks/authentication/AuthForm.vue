<script setup lang="ts">
import { ref, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { useAuth } from "@/composables/auth"
import { useAuthPageStore } from "@/stores/Authentication/authPageStore"
// assets
import googleIcon from '@/assets/icons/google-icon.svg'
import { Loader2 } from 'lucide-vue-next'


const auth = useAuth()
const authPageStore = useAuthPageStore()

const email = ref('')
const password = ref('')
const name = ref('')

watch(
  () => auth.errorMessage,
  (newValue) => {
    console.log('Error message changed:', newValue)
    if (newValue) {
      setTimeout(() => {
        auth.clearError()
      }, 3000)
    }
  },
  { immediate: true }
)


</script>
<template>

  <div v-show="true" class="max-w-md w-full bg-white p-10 rounded-xl shadow-lg">
    <!-- Logo -->
    <div class="text-center ">
      <h2 v-if="authPageStore.isStudent" class="text-3xl font-bubblegum font-bold text-amber-500 "
        data-test-id=form-title>
        {{
          authPageStore.isLogin ?
            'Student log in' : 'Sign up to play!'
        }}</h2>
      <h2 v-else class="text-3xl font-bubblegum font-bold text-blue-500 " data-test-id=form-title>
        {{
          authPageStore.isLogin ?
            'Welcome Back, Educator!' : 'Join as an Educator'
        }}</h2>


      <p v-if="authPageStore.isStudent" class="mt-2 text-gray-600" data-test-id="form-description">
        {{ authPageStore.isLogin ? 'Welcome back!' : 'Join the fun!' }}
      </p>
      <p v-else class="mt-2 text-gray-600" data-test-id="form-description">
        {{ authPageStore.isLogin ? 'Continue your teaching journey'
          : 'Start empowering students today' }}
      </p>
    </div>

    <!-- Form -->
    <form class="" @submit.prevent="() => auth.handleSubmit(email, password, name)">

      <div class="space-y-4 mt-5">
        <div v-if="!authPageStore.isLogin" key="name" class="">
          <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
          <input id="name" v-model="name" type="text" required
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>

        <!-- Email Field -->
        <div key="email" class="">
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <input id="email" v-model="email" type="email" required @focus="auth.clearError"
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>

        <!-- Password Field -->
        <div key="password" class="">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input id="password" v-model="password" type="password" required @focus="auth.clearError"
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <!-- Registration Name Field -->

        <!-- Error Message -->
        <p v-if="auth.errorMessage" key="error"
          class="mt-2 text-sm text-red-600 transition-all text-center duration-300">
          {{ auth.errorMessage }}
        </p>
      </div>



      <!-- Action Buttons -->

      <div class="space-y-1 mt-4">
        <!-- Submit Button -->
        <Button type="submit" :disabled="authPageStore.emailLoading || authPageStore.googleLoading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          :class="!authPageStore.isStudent ? ' bg-blue-600 hover:bg-blue-700  focus:ring-blue-500' : 'bg-amber-500 hover:bg-amber-600 focus:ring-amber-500'">

          <Loader2 v-if="authPageStore.emailLoading" class="animate-spin mr-2" />
          {{ authPageStore.isLogin ? 'Sign In' : 'Create Account' }}
        </Button>

        <!-- Divider -->
        <div class="relative my-4">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>

        <!-- Login via Google -->
        <Button type="button" @click="auth.handleGoogle"
          :disabled="authPageStore.emailLoading || authPageStore.googleLoading"
          class="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md border border-gray-300 shadow-sm text-sm font-medium text-gray-600 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          <Loader2 v-if="authPageStore.googleLoading" class="animate-spin mr-2" />
          <img v-else :src="googleIcon" alt="Google Icon" class="w-5 h-5" />
          {{ !authPageStore.isLogin ? "Sign up with Google" : "Sign in with Google" }}
        </Button>
        <!-- Toggle Form -->
        <div class="text-center mt-5">
          <button type="button" class="text-sm text-blue-600 hover:text-blue-500" @click="authPageStore.toggleForm"
            data-test-id="toggle-form">
            {{ authPageStore.isLogin ? 'Need an account? Sign up' : 'Already have an account? Sign in' }}
          </button>
        </div>
      </div>
    </form>
  </div>

</template>
