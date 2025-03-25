<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { auth } from '@/config/firebaseConfig'
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword } from 'firebase/auth'
// services
import { SignUser, LoginUser } from '@/services/AuthService'
// assets
import googleIcon from '@/assets/icons/google-icon.svg'
// types
import type { DecodedToken } from "@/types/miscellaneous"


const isLogin = ref(true)
const email = ref('')
const password = ref('')
const name = ref('')
const errorMessage = ref('')

const { replace } = useRouter()
const provider = new GoogleAuthProvider();

const toggleForm = () => {
  isLogin.value = !isLogin.value
  email.value = ''
  password.value = ''
  name.value = ''
}

const clearError = () => {
  errorMessage.value = ''
}

const handleGoogle = async () => {
  try {

    const userCredential = await signInWithPopup(auth, provider)
    const idToken = (await userCredential.user.getIdTokenResult()).token

    // login the user
    if (isLogin.value) {

      const user = {
        email: userCredential.user.email || "",
        uid: userCredential.user.uid,
      }

      LoginUser(user, idToken)
        .then((res) => {
          console.log(res)
          replace('/student')
        })
        .catch((error) => console.error(error))
    }
    else {
      // sign up the user

      const name = jwtDecode<DecodedToken>(idToken).name
      const email = jwtDecode<DecodedToken>(idToken).email

      const user = {
        name: name,
        email: email,
        uid: userCredential.user.uid,
        role: 'student' as const
      }

      console.log(user, idToken, userCredential)

      // save user to database
      await SignUser(user, idToken)
        .then(() => {
          replace('/student')
        })
        .catch((err) => console.error(err))
    }

  } catch (error: unknown) {
    console.error(error)
  }

}


const handleSubmit = async () => {
  // login flow
  if (isLogin.value) {

    try {
      console.log(email.value, password.value)
      const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value)

      const user = {
        email: email.value,
        uid: userCredential.user.uid,
      }

      const idToken = (await userCredential.user.getIdTokenResult()).token

      // login the user
      if (idToken) LoginUser(user, idToken).then(() => replace('/educator')).catch(error => console.error(error))

    } catch (error: unknown) {

      const firebaseError = error as { code: string };
      if (firebaseError.code === 'auth/invalid-credential') {
        errorMessage.value = 'Invalid email or password'
      } else if (firebaseError.code === 'auth/weak-password') {
        errorMessage.value = 'Password should be at least 6 characters'
      } else {
        errorMessage.value = 'An error occurred. Please try again.'
      }
      console.error(firebaseError)
    }
    return

  }

  // signup flow
  try {

    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value)

    const idToken = await userCredential.user.getIdToken()

    const user = {
      name: name.value,
      email: email.value,
      uid: userCredential.user.uid,
      role: "educator" as const
    }

    console.log(user, userCredential.user)

    // save user to database
    await SignUser(user, idToken)
      .then(() => {
        replace('/educator')
      })
      .catch((err) => console.error(err))

    alert("Signed up successfully!")
  } catch (error: unknown) {
    const firebaseError = error as { code: string };
    if (firebaseError.code === 'auth/email-already-in-use') {
      errorMessage.value = 'Email already registered'
    } else if (firebaseError.code === 'auth/weak-password') {
      errorMessage.value = 'Password should be at least 6 characters'
    } else {
      errorMessage.value = 'An error occurred. Please try again.'
    }
    console.error(firebaseError)

  }


}



</script>
<template>

  <div v-show="true" class="max-w-md w-full bg-white p-10 rounded-xl shadow-lg">
    <!-- Logo -->
    <div class="text-center ">
      <h2 class="text-3xl font-bubblegum font-bold text-blue-500 ">
        {{ isLogin ? 'Welcome Back, Educator!' : 'Join as an Educator' }}</h2>
      <p class="mt-2 text-gray-600">{{ isLogin ? 'Continue your teaching journey' : 'Start empowering students today' }}
      </p>
    </div>

    <!-- Form -->
    <form class="  " @submit.prevent="handleSubmit">

      <div class="space-y-4 mt-5">
        <div v-if="!isLogin" key="name" class="">
          <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
          <input id="name" v-model="name" type="text" required
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>

        <!-- Email Field -->
        <div key="email" class="">
          <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
          <input id="email" v-model="email" type="email" required @focus="clearError"
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>

        <!-- Password Field -->
        <div key="password" class="">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input id="password" v-model="password" type="password" required @focus="clearError"
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <!-- Registration Name Field -->

        <!-- Error Message -->
        <p v-if="errorMessage" key="error" class="mt-2 text-sm text-red-600 transition-all text-center duration-300">
          {{ errorMessage }}
        </p>
      </div>



      <!-- Action Buttons -->

      <div class="space-y-1 mt-4">
        <!-- Submit Button -->
        <button type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ">
          {{ isLogin ? 'Sign In' : 'Create Account' }}
        </button>

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
        <button type="button" @click="handleGoogle"
          class="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md border border-gray-300 shadow-sm text-sm font-medium text-gray-600 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          <img :src="googleIcon" alt="Google Icon" class="w-5 h-5" />
          {{ !isLogin ? "Sign up with Google" : "Sign in with Google" }}
        </button>
        <!-- Toggle Form -->
        <div class="text-center mt-5">
          <button type="button" class="text-sm text-blue-600 hover:text-blue-500" @click="toggleForm">
            {{ isLogin ? 'Need an account? Sign up' : 'Already have an account? Sign in' }}
          </button>
        </div>
      </div>
    </form>
  </div>

</template>
