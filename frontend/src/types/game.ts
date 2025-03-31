import type { Activity } from './activity'

export interface Game {
  id: string
  title: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  age_range: string
  image: string
  activities: Activity[]
  target_range: [number, number]
  total_points: number
  template: boolean
}

export interface WeighingObject {
  id: string
  weight: number
  image?: string
  type: string
  location: 'available' | 'left' | 'right'
}

export interface GameLevel {
  id: number
  objects: WeighingObject[]
  target?: number
  difficulty: 'easy' | 'medium' | 'hard'
}
