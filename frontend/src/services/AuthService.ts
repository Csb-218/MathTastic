import AxiosInstance from '@/config/axiosConfig'
import type { AxiosResponse } from 'axios'
import type { user, user_login } from '@/types/user'

export async function SignUser(user: user, token: string) {
  const response = await AxiosInstance.post('/users/register', user, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response
}

export async function LoginUser(user: user_login, token: string) {
  const response: AxiosResponse = await AxiosInstance.post('/users/login', user, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  return response
}

export async function checkAuthentication(cookie: string) {
  const response = await AxiosInstance.get('/users/check-auth', {
    headers: {
      user_cookie: cookie,
    },
  })
  return response
}
