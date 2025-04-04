import AxiosInstance from '@/config/axiosConfig'
import type { Activity } from '@/types/activity'

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

// add activity to game
export async function addActivityToGame(id: string, activity_id: Activity) {
  try {
    const requestBody = {
      activity_ids: [activity_id],
    }

    const response = await AxiosInstance.patch(`/games/${id}/activities`, requestBody)

    return response.data
  } catch (error) {
    console.error(error)
  }
}

// create activity
export async function createActivity(activity: Activity) {
  try {
    const response = await AxiosInstance.post('/activities/create', activity)
    return response.data
  } catch (error) {
    console.error(error)
  }
}
