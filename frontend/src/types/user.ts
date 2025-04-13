export type user = {
  name: string
  email: string
  uid: string
  role: 'admin' | 'student' | 'educator'
}

export interface user_state {
  name: string
  session: string | null
  email: string
  role: string
  uid: string
}

export type user_login = {
  email: string
  uid: string
}
