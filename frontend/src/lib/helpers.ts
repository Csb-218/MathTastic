import appleIcon from '@/assets/game/apple.svg'
import bananaIcon from '@/assets/game/banana.svg'
import orangeIcon from '@/assets/game/orange.svg'
import type { WeighingObject } from '@/types/game'
import type { Activity } from '@/types/activity'
export function getSessionCookie(): string | undefined {
  const cookies = document.cookie.split(';')
  const sessionCookie = cookies.find((cookie) => cookie.trim().startsWith('user'))
  return sessionCookie
}

// random object icon allocator
export function getRandomObjectIcon(): string {
  const icons = [appleIcon, bananaIcon, orangeIcon]
  const randomIndex = Math.floor(Math.random() * icons.length)
  return icons[randomIndex]
}

// create weighing objects from activity
export function createWeighingObjectsFromActivity(activity: Activity): WeighingObject[] {
  const weighingObjects: WeighingObject[] = []

  // Process each addend and create corresponding objects
  activity.addends.forEach((weight, index) => {
    const obj: WeighingObject = {
      id: `obj-${index}`,
      weight,
      type: 'fruit',
      image: getRandomObjectIcon(),
      location: 'available',
    }
    weighingObjects.push(obj)
  })

  return weighingObjects
}
