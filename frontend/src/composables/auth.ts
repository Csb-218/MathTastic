import { ref } from 'vue'
import { jwtDecode } from 'jwt-decode'
import { useRouter } from 'vue-router'
import { auth } from '@/config/firebaseConfig'
import {
  createUserWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
} from 'firebase/auth'
import type { UserCredential } from 'firebase/auth'
import { useAuthStore } from '@/stores/Authentication/authStore'
import { useAuthPageStore } from '@/stores/Authentication/authPageStore'
import type { DecodedIdToken } from '@/types/miscellaneous'
import type { user, user_login, user_operation } from '@/types/user'
import { AxiosError } from 'axios'

export function useAuth() {
  const errorMessage = ref('')
  const router = useRouter()
  const provider = new GoogleAuthProvider()
  const { login_user, register_user } = useAuthStore()
  const authPageStore = useAuthPageStore()

  const clearError = () => (errorMessage.value = '')

  const handleFirebaseError = (error: { code: string }) => {
    const errorMessages: Record<string, string> = {
      'auth/invalid-credential': 'Invalid email or password',
      'auth/weak-password': 'Password should be at least 6 characters',
      'auth/email-already-in-use': 'Email already registered',
    }
    errorMessage.value = errorMessages[error.code] || 'An error occurred. Please try again.'
    console.error(error)
  }

  const redirectUser = () => {
    const path = authPageStore.student ? '/student' : '/educator'
    router.replace(path)
  }

  const createLoginUser = (credential: UserCredential): user_login => ({
    email: credential.user.email || '',
    uid: credential.user.uid,
  })

  const createRegisterUser = (credential: UserCredential, name: string, email: string): user => ({
    name,
    email,
    uid: credential.user.uid,
    role: authPageStore.student ? 'student' : 'educator',
  })

  const handleAuthFlow = async (
    user: user | user_login,
    idToken: string,
    operation: user_operation,
  ) => {
    try {
      if (operation === 'login') {
        await login_user(user, idToken)
      } else {
        await register_user(user as user, idToken).then(async () => await login_user(user, idToken))
      }
      redirectUser()
    } catch (error) {
      console.error(error)
      if (error instanceof AxiosError) {
        errorMessage.value = error.response?.data?.detail
      }
    }
  }

  const handleGoogle = async () => {
    try {
      authPageStore.setGoogleLoading(true)
      const credential = await signInWithPopup(auth, provider)
      const idToken = (await credential.user.getIdTokenResult()).token

      if (authPageStore.login) {
        const user = createLoginUser(credential)
        await handleAuthFlow(user, idToken, 'login')
      } else {
        const decodedToken = jwtDecode<DecodedIdToken>(idToken)
        const user = createRegisterUser(credential, decodedToken.name, decodedToken.email)
        await handleAuthFlow(user, idToken, 'register')
      }
    } catch (error) {
      console.error(error)
    } finally {
      authPageStore.setGoogleLoading(false)
    }
  }

  const handleSubmit = async (email: string, password: string, name: string) => {
    try {
      authPageStore.setEmailLoading(true)
      if (authPageStore.login) {
        const credential = await signInWithEmailAndPassword(auth, email, password)
        const idToken = (await credential.user.getIdTokenResult()).token
        const user = createLoginUser(credential)
        await handleAuthFlow(user, idToken, 'login')
      } else {
        const credential = await createUserWithEmailAndPassword(auth, email, password)
        const idToken = await credential.user.getIdToken()
        const user = createRegisterUser(credential, name, email)
        await handleAuthFlow(user, idToken, 'register')
        alert('Signed up successfully!')
      }
    } catch (error) {
      handleFirebaseError(error as { code: string })
    } finally {
      authPageStore.setEmailLoading(false)
    }
  }

  return {
    handleGoogle,
    handleSubmit,
    errorMessage,
    clearError,
  }
}
