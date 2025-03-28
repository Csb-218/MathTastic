import AxiosInstance from '@/config/axiosConfig'

// get all games
export async function getAllGames() {
  try {
    const response = await AxiosInstance.get('/games')
    return response.data
  } catch (error) {
    console.error(error)
  }
}
// get game by id
export async function getGameById(id: string) {
  try {
    const response = await AxiosInstance.get(`/games/${id}`)
    return response.data
  } catch (error) {
    console.error(error)
  }
}
