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
                replace('/student')
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
            console.log(1)
            const user = {
                email: email.value,
                uid: userCredential.user.uid,
            }
            console.log(2)
            const idToken = (await userCredential.user.getIdTokenResult()).token
            console.log(3)
            // login the user
            if (idToken) LoginUser(user, idToken)

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
            role: 'student' as 'student'
        }

        console.log(user, userCredential.user)

        // save user to database
        await SignUser(user, idToken)
            .then(() => {
                replace('/student')
            })
            .catch((err) => console.error(err))

        alert("Signed up successfully!")
        console.log(userCredential)
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
    <Transition enter-active-class="transition ease-out duration-300" enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-200"
        leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
        <div v-show="true" class="max-w-md w-full space-y-10 bg-white p-8 rounded-xl shadow-lg">
            <!-- Logo -->
            <div class="text-center">
                <h2 class="text-3xl font-fredoka font-bold text-amber-500 ">
                    {{ isLogin ? 'Student log in' : 'Sign up toplay!' }}</h2>
                <p class="mt-2 text-gray-600">{{ isLogin ? 'Welcome back!' : 'Join the fun!' }}</p>
            </div>

            <!-- Form -->
            <form class="flex flex-col gap-y-4" @submit.prevent="handleSubmit">
                <TransitionGroup enter-active-class="transition-all duration-300 ease-out"
                    enter-from-class="opacity-0 -translate-y-4" enter-to-class="opacity-100 translate-y-0"
                    leave-active-class="transition-all duration-300 ease-in"
                    leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-4">
                    <!-- Registration Name Field -->
                    <div v-if="!isLogin" key="name" class="mb-10">
                        <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                        <input id="name" v-model="name" type="text" required
                            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500" />
                    </div>

                    <!-- Email Field -->
                    <div key="email" class="">
                        <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                        <input id="email" v-model="email" type="email" required @focus="clearError"
                            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500" />
                    </div>

                    <!-- Password Field -->
                    <div key="password" class="">
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input id="password" v-model="password" type="password" required @focus="clearError"
                            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500" />
                        <!-- Error Message -->
                        <p v-if="errorMessage" key="error"
                            class="mt-2 text-sm text-red-600 transition-all text-center duration-300">
                            {{ errorMessage }}
                        </p>
                    </div>

                </TransitionGroup>

                <!-- Submit Button -->
                <button type="submit"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 mt-8">
                    {{ isLogin ? 'Sign In' : 'Create Account' }}
                </button>

                <!-- Login via Google -->
                <button type="button" @click="handleGoogle"
                    class="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md border border-gray-300 shadow-sm text-sm font-medium text-gray-600 bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2">
                    <img :src="googleIcon" alt="Google Icon" class="w-5 h-5" />
                    {{ !isLogin ? "Sign up with Google" : "Sign in with Google" }}
                </button>


                <!-- Toggle Form -->
                <div class="text-center mt-5">
                    <button type="button" class="text-sm text-amber-600 hover:text-amber-500" @click="toggleForm">
                        {{ isLogin ? 'Need an account? Sign up' : 'Already have an account? Sign in' }}
                    </button>
                </div>
            </form>
        </div>
    </Transition>
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