import type { activity } from './activity'
export type Game = {
  id: number
  title: string
  description: string
  activities: [activity]
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
  color: string
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
