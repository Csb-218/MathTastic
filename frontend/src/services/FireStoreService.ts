import { db } from '@/config/firebaseConfig'
import {
  collection,
  addDoc,
  where,
  query,
  getDocs,
  updateDoc,
  doc,
  increment,
  onSnapshot,
} from 'firebase/firestore'
import type { progress, progress_object } from '@/types/progress'

export async function createProgress(progressObject: progress): Promise<string> {
  try {
    const docRef = await addDoc(collection(db, 'progress'), progressObject)
    return docRef.id
  } catch (err) {
    console.error(err)
    return ''
  }
}

export async function updateProgress(progressObject: progress) {
  try {
    // First get the document reference using student_uid
    const progress_collection = collection(db, 'progress')
    const q = query(progress_collection, where('student_uid', '==', progressObject.student_uid))
    const querySnapshot = await getDocs(q)

    if (querySnapshot.empty) {
      throw new Error('No document found for this student_uid')
    }

    // Get the actual document ID
    const docId = querySnapshot.docs[0].id

    // Update using the correct document ID
    const docRef = doc(db, 'progress', docId)
    await updateDoc(docRef, {
      games_played: progressObject.games_played,
      points: increment(progressObject.points),
    })

    console.log('Document successfully updated!')
  } catch (err) {
    console.error('Error updating document: ', err)
    throw err // Re-throw to handle in calling code
  }
}

export async function getProgressByStudentUid(studentUid: string): Promise<progress_object | null> {
  try {
    const progress_collection = collection(db, 'progress')
    const q = query(progress_collection, where('student_uid', '==', studentUid))

    const querySnapshot = await getDocs(q)
    if (querySnapshot.empty) {
      console.log('No matching documents.')
      return null
    }

    console.log(querySnapshot.docs)

    const student_progress: progress = querySnapshot.docs[0].data() as progress
    const id: string = querySnapshot.docs[0].id

    return {
      id,
      data: student_progress,
    } as progress_object
  } catch (err) {
    console.error(err)
    return null
  }
}

export async function listenToProgress(id: string) {
  const unsub = onSnapshot(doc(db, 'progress', id), (doc) => {
    console.log('Current data: ', doc.data())
  })
  return unsub
}
