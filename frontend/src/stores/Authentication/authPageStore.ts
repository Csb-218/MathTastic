import type { user_auth } from '@/types/user'
import { defineStore } from 'pinia'

export const useAuthPageStore = defineStore('authPage', {
  state: (): user_auth => {
    return {
      student: true,
      admin: false,
      login: true,
      emailLoading: false,
      googleLoading: false,
    }
  },
  getters: {
    isStudent: (state) => state.student,
    isAdmin: (state) => state.admin,
    isLogin: (state) => state.login,
  },
  actions: {
    setStudent(value: boolean) {
      this.student = value
    },

    setAdmin(value: boolean) {
      this.admin = value
    },
    setLogin(value: boolean) {
      this.login = value
    },
    setEmailLoading(value: boolean) {
      this.emailLoading = value
    },
    setGoogleLoading(value: boolean) {
      this.googleLoading = value
    },

    toggleForm() {
      this.login = !this.login
    },

    reset() {
      this.student = false
      this.admin = false
      this.login = false
    },
  },
})
