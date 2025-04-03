import {
  appleIcon,
  bananaIcon,
  orangeIcon,
  beetrootIcon,
  grapesIcon,
  strawberryIcon,
  watermelonIcon,
  mushroomIcon,
} from '@/assets/game'
import type { WeighingObject } from '@/types/game'
import type { Activity } from '@/types/activity'

const fruitIcons = [
  appleIcon,
  bananaIcon,
  orangeIcon,
  beetrootIcon,
  grapesIcon,
  strawberryIcon,
  watermelonIcon,
  mushroomIcon,
]

export function getSessionCookie(): string | undefined {
  const cookies = document.cookie.split(';')
  const sessionCookie = cookies.find((cookie) => cookie.trim().startsWith('user'))
  return sessionCookie
}

// create weighing objects from activity
export function createWeighingObjectsFromActivity(activity: Activity): WeighingObject[] {
  const weighingObjects: WeighingObject[] = []

  // Create a map to store weight-to-icon mappings
  const weightToImageMap = new Map<number, string>()

  // Process each addend and create corresponding objects
  activity.addends.forEach((weight, index) => {
    // Get or assign an icon for this weight
    let iconToUse: string

    if (weightToImageMap.has(weight)) {
      // Use existing icon for same weights
      iconToUse = weightToImageMap.get(weight)!
    } else {
      // Assign new icon from the pool
      iconToUse = fruitIcons[weightToImageMap.size % fruitIcons.length]
      weightToImageMap.set(weight, iconToUse)
    }

    // Create weighing object
    const obj: WeighingObject = {
      id: `obj-${index}`,
      weight,
      type: 'fruit',
      image: iconToUse,
      location: 'available',
    }
    weighingObjects.push(obj)
  })

  return weighingObjects
}
