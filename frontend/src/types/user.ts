export type role = 'admin' | 'student' | 'educator'

export interface user {
  name: string
  email: string
  uid: string
  role: role
}

export interface user_state {
  name: string
  session: string | null
  email: string
  role: string
  uid: string
  picture: string | null
}

export type user_login = {
  email: string
  uid: string
}

export type user_auth = {
  student: boolean
  admin: boolean
  login: boolean
  emailLoading: boolean
  googleLoading: boolean
}

export type user_operation = 'login' | 'register'
