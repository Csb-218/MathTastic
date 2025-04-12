import AxiosInstance from '@/config/axiosConfig'
import type { user, login } from '@/types/user'

export async function SignUser(user: user, token: string) {
  console.log(user, token)
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

export async function LoginUser(user: login, token: string) {
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
