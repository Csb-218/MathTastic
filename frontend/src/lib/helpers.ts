import appleIcon from '@/assets/game/apple.svg'
import bananaIcon from '@/assets/game/banana.svg'
import orangeIcon from '@/assets/game/orange.svg'
import type { WeighingObject } from '@/types/game'
import type { Activity } from '@/types/activity'

const fruitIcons = [appleIcon, bananaIcon, orangeIcon]

export function getSessionCookie(): string | undefined {
  const cookies = document.cookie.split(';')
  const sessionCookie = cookies.find((cookie) => cookie.trim().startsWith('user'))
  return sessionCookie
}

// create weighing objects from activity
export function createWeighingObjectsFromActivity(activity: Activity): WeighingObject[] {
  const weighingObjects: WeighingObject[] = []
  const weightToImageMap = new Map<number, string>()

  // Process each addend and create corresponding objects
  activity.addends.forEach((weight, index) => {
    // If this weight hasn't been assigned an image yet, assign one
    if (!weightToImageMap.has(weight)) {
      const unusedIcons = fruitIcons.filter(
        (icon) => !Array.from(weightToImageMap.values()).includes(icon),
      )

      // If we've used all icons, start over with the first one
      const iconToUse =
        unusedIcons.length > 0
          ? unusedIcons[0]
          : fruitIcons[weightToImageMap.size % fruitIcons.length]

      weightToImageMap.set(weight, iconToUse)
    }

    const obj: WeighingObject = {
      id: `obj-${index}`,
      weight,
      type: 'fruit',
      image: weightToImageMap.get(weight)!,
      location: 'available',
    }
    weighingObjects.push(obj)
  })

  return weighingObjects
}
