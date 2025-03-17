import axios from 'axios'
const AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_SERVER_BaseUrl,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true

})

export default AxiosInstance