import AxiosInstance from '@/config/axiosConfig'
import type { user, user_login } from '@/types/user'

export async function SignUser(user: user, token: string) {
  try {
    const response = await AxiosInstance.post('/users/register', user, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return response
  } catch (err) {
    console.log(err)
  }
}

export async function LoginUser(user: user_login, token: string) {
  try {
    const response = await AxiosInstance.post('/users/login', user, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return response
  } catch (e) {
    console.error(e)
  }
}

export async function checkAuthentication(cookie: string) {
  try {
    const response = await AxiosInstance.get('/users/check-auth', {
      headers: {
        user_cookie: cookie,
      },
    })
    return response
  } catch (e) {
    console.error(e)
  }
}
