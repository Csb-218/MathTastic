import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import { getSessionCookie } from '@/lib/helpers'
import { LoginUser, SignUser } from '@/services/AuthService'
// types
import type { user_login, user_state, user } from '@/types/user'
import type { DecodedToken } from '@/types/miscellaneous'

export const useAuthStore = defineStore('auth', {
  state: (): user_state => {
    return {
      session: getSessionCookie(),
      name: '',
      email: '',
      role: '',
      uid: '',
    }
  },
  getters: {
    is_authenticated: (state) => {
      return state.session !== ''
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
    async login_user(user: user_login, idToken: string): Promise<void> {
      try {
        const response = await LoginUser(user, idToken)
        const token = response?.data.token
        await this.init(token)
      } catch (error) {
        console.error('Login failed:', error)
      }
    },

    async register_user(user_register: user, idToken: string): Promise<void> {
      try {
        await SignUser(user_register, idToken)
      } catch (error) {
        console.error('Login failed:', error)
      }
    },

    async init(token: string): Promise<void> {
      try {
        const { sub, exp } = jwtDecode<DecodedToken>(token)

        // Check if the token is expired
        if (exp < Date.now() / 1000) {
          console.error('Token expired')
          this.logout()
          return
        }
        // Set the session cookie with age expiration
        document.cookie = `user_cookie=${token}; path=/; max-age=3600` // 1 hour expiration
        // Set the user data
        this.session = token
        this.name = sub.name
        this.email = sub.email
        this.role = sub.role
        this.uid = sub.uid
      } catch (error) {
        console.error('Failed to initialize session:', error)
      }
    },

    logout() {
      // Remove the cookie by setting its expiration to past date
      document.cookie = 'user_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      this.session = ''
      this.name = ''
      this.email = ''
      this.role = ''
      this.uid = ''
    },
  },
})
