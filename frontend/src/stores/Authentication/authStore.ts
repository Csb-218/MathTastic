import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { getSessionCookie } from '@/lib/helpers'
import { LoginUser, SignUser } from '@/services/AuthService'
// types
import type { user_login, user_state, user } from '@/types/user'
import type { DecodedToken } from '@/types/miscellaneous'

interface DecodedIdToken {
  picture: string
}
export const useAuthStore = defineStore('auth', {
  state: (): user_state => {
    return {
      session: getSessionCookie(),
      name: '',
      email: '',
      role: '',
      uid: '',
      picture: null,
    }
  },
  getters: {
    is_authenticated: (state) => {
      return state.session !== null
    },
    is_admin: (state) => {
      return state.role === 'admin'
    },
    is_student: (state) => {
      return state.role === 'student'
    },
    is_educator: (state) => {
      return state.role === 'educator'
    },
    get_user: (state) => {
      return state
    },
  },
  actions: {
    async login_user(user: user_login, idToken: string) {
      const response = await LoginUser(user, idToken)
      const token = response?.data.token
      // storing firebase token in cookie
      document.cookie = `firebase_cookie=${idToken}; path=/; max-age=3600`
      await this.init(token, idToken)
    },

    async register_user(user_register: user, idToken: string): Promise<void> {
      await SignUser(user_register, idToken)
    },

    async init(token: string, idToken: string | null): Promise<void> {
      const { sub, exp } = jwtDecode<DecodedToken>(token)

      // Check if the token is expired
      if (exp < Date.now() / 1000) {
        console.error('Token expired')
        this.logout()
        return
      }

      if (idToken) {
        const { picture } = jwtDecode<DecodedIdToken>(idToken)
        this.picture = picture
      }

      // Set the session cookie with age expiration
      document.cookie = `user_cookie=${token}; path=/; max-age=3600` // 1 hour expiration

      // Set the user data
      this.session = token
      this.name = sub.name
      this.email = sub.email
      this.role = sub.role
      this.uid = sub.uid
    },

    logout() {
      // Remove the cookie by setting its expiration to past date
      document.cookie = 'user_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      this.session = ''
      this.name = ''
      this.email = ''
      this.role = ''
      this.uid = ''
      console.log('User logged out')
    },
  },
})
