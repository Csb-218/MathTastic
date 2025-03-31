import { db } from '@/config/firebaseConfig'
import {
  collection,
  addDoc,
  updateDoc,
  doc,
  getDocs,
  query,
  where,
  increment,
} from 'firebase/firestore'
import type { game_progress, progress_object } from '@/types/progress'

export async function createProgress(uid: string, game: game_progress): Promise<string> {
  try {
    // Get a reference to the user's document in the progress collection
    const userRef = doc(collection(db, 'progress'), uid)

    // Create games_played subcollection within the user's document
    const gamesPlayedRef = collection(userRef, 'games_played')

    const gameDoc = await addDoc(gamesPlayedRef, {
      ...game,
      created_at: new Date(),
      updated_at: new Date(),
    })

    return gameDoc.id
  } catch (err) {
    console.error(err)
    throw err
  }
}

export async function updateProgress(
  uid: string,
  progress_id: string,
  updates: Partial<game_progress>,
) {
  try {
    // Get direct reference to the game document
    const gameDocRef = doc(db, 'progress', uid, 'games_played', progress_id)

    await updateDoc(gameDocRef, {
      current_level: updates.current_level,
      points_gained: increment(updates?.points_gained ?? 0),
      updated_at: new Date(),
    })

    console.log('Game progress successfully updated!')
  } catch (err) {
    console.error('Error updating game progress:', err)
    throw err
  }
}

export async function getProgressByStudentUid(
  uid: string,
  game_id: string,
): Promise<progress_object | null> {
  try {
    const userRef = doc(collection(db, 'progress'), uid)

    const gamesPlayedRef = collection(userRef, 'games_played')

    const q = query(gamesPlayedRef, where('game_id', '==', game_id))

    const gameDoc = await getDocs(q)

    if (gameDoc.empty) {
      console.log('No matching game found.')
      return null
    }

    const progress_values: progress_object = {
      data: gameDoc.docs[0].data() as game_progress,
      id: gameDoc.docs[0].id,
    }

    return progress_values
  } catch (err) {
    console.error('Error getting game progress:', err)
    return null
  }
}

export async function resetProgress(uid: string, progress_id: string) {
  try {
    const gameDocRef = doc(db, 'progress', uid, 'games_played', progress_id)

    await updateDoc(gameDocRef, {
      current_level: 0,
      points_gained: 0,
      updated_at: new Date(),
    })

    console.log('Game progress successfully reset!')
  } catch (err) {
    console.error('Error resetting game progress:', err)
  }
}
