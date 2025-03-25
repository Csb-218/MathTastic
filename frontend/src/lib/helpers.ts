import type { WeighingObject } from '@/types/game'
export function getSessionCookie(): string | undefined {
  const cookies = document.cookie.split(';')
  const sessionCookie = cookies.find((cookie) => cookie.trim().startsWith('user'))
  return sessionCookie
}
// Helper function for object styling
export const getObjectStyle = (obj: WeighingObject) => {
  if (obj.image) {
    return {}
  }
  return {
    backgroundColor: obj.color,
  }
}
