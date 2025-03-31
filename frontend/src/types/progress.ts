export interface game_progress {
  game_id: string
  current_level: number
  total_levels: number | null
  points_gained: number
  total_points: number | null
}

export interface progress_object {
  id: string
  data: game_progress
}
