import type { Game } from './game'
import type { Activity } from './activity'

export interface progress {
  student_uid: string
  games_played: game_progress[]
  points: number
}

export interface game_progress {
  game: Game
  current_level: number
  completed_activities: Activity[]
}
