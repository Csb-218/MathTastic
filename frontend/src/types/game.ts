import type { Activity } from './activity'

export interface Game {
  id: number
  title: string
  description: string
  activities: Activity[]
  image: string
  level: string
  ageRange: string
  targetRange: [number, number]
  totalPoints: number
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
