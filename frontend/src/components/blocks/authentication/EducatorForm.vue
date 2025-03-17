<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '@/config/firebaseConfig'
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword } from 'firebase/auth'

// services
import { SignUser, LoginUser } from '@/services/AuthService'
// assets
import googleIcon from '@/assets/google-icon.svg'


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
        const user = {
            email: userCredential.user.email || "",
            uid: userCredential.user.uid,
        }

        const idToken = (await userCredential.user.getIdTokenResult()).token

        LoginUser(user, idToken)
            .then((res) => {
                console.log(res)
                replace('/educator')
            })
            .catch((error) => console.error(error))
        console.log(userCredential)
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
            role: "educator" as "educator"
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
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-xl border border-blue-100">
        <!-- Header -->
        <div class="text-center">
            <h2 class="text-3xl font-bold text-blue-600">
                {{ isLogin ? 'Welcome Back, Educator!' : 'Join as an Educator' }}
            </h2>
            <p class="mt-3 text-gray-600">
                {{ isLogin ? 'Continue your teaching journey' : 'Start empowering students today' }}
            </p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="mt-8 flex flex-col gap-y-4">
            <div class="space-y-5">
                <!-- Name Field (Signup only) -->
                <div v-if="!isLogin">
                    <label for="name" class="block text-sm font-medium text-gray-700">Full Name</label>
                    <input id="name" v-model="name" type="text" required
                        class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                </div>
                <!-- Email Field -->
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                    <input id="email" v-model="email" type="email" required @focus="clearError"
                        class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                </div>

                <!-- Password Field -->
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                    <input id="password" v-model="password" type="password" required @focus="clearError"
                        class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500" />
                </div>

                <!-- Error Message -->
                <div v-if="errorMessage" class="text-center">
                    <p class="text-sm text-red-600">{{ errorMessage }}</p>
                </div>
            </div>


            <!-- Submit Button -->
            <button type="submit"
                class="w-full py-3 px-4 border border-transparent rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                {{ isLogin ? 'Sign In' : 'Create Account' }}
            </button>

            <!-- Login via Google -->
            <button type="button" @click="handleGoogle"
                class="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md border border-gray-300 shadow-sm text-sm font-medium text-gray-600 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2">
                <img :src="googleIcon" alt="Google Icon" class="w-5 h-5" />
                {{ isLogin ? "Sign up with Google" : "Sign in with Google" }}
            </button>

            <!-- Toggle Form -->
            <div class="text-center mt-4">
                <button type="button" class="text-sm text-blue-600 hover:text-blue-500" @click="toggleForm">
                    {{ isLogin ? 'New educator? Create an account' : 'Already have an account? Sign in' }}
                </button>
            </div>
        </form>
    </div>

</template>
