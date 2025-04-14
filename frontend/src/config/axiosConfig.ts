import axios from 'axios'
const AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_HOST,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

export default AxiosInstance
