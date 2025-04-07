export interface Activity {
  _id: string
  level: number
  target: number
  addends: number[]
  addends_size: number
  time_limit: number
  hints: string[]
  points: number
  success_feedback: string
  failure_feedback: string
}
