import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import AxiosInstance from "@/config/axiosConfig"
import { jwtDecode } from 'jwt-decode'

interface DecodedToken {
    name: string;
    email: string;
    role: string;
}
// types
import type { user_state } from "@/types/user"

export const useAuthStore = defineStore('auth', {
    state: (): user_state => {
        return {
            session: '',
            name: '',
            email: '',
            role: ''
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
        }

    },
    actions: {
        login_user(user_data: user_state) {
            if (user_data.session) this.session = user_data.session
            if (user_data.name) this.name = user_data.name
            if (user_data.role) this.role = user_data.role
        },

        async init(cookie: string): Promise<void> {
            try {
                const token = cookie.split('=')[1] // Get token value from cookie
                const decoded_token = jwtDecode<DecodedToken>(token)

                if (decoded_token) {
                    this.login_user({
                        session: token,
                        name: decoded_token.name,
                        email: decoded_token.email,
                        role: decoded_token.role
                    })
                }

            } catch (error) {
                console.error('Failed to initialize session:', error)
            }
        },

        logout() {
            // Remove the cookie by setting its expiration to past date
            document.cookie = "user_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
            this.session = ''
            this.name = ''
            this.email = ''
            this.role = ''
        }


    },
})