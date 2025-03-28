import { db } from '@/config/firebaseConfig'
import { collection, addDoc, where, query, getDocs, updateDoc, doc } from 'firebase/firestore'
import type { progress } from '@/types/progress'

export async function createProgress(progressObject: progress) {
  try {
    const docRef = await addDoc(collection(db, 'progress'), progressObject)
    console.log('Document written with ID: ', docRef.id)
    return docRef.id
  } catch (err) {
    console.error(err)
  }
}

export async function updateProgress(progressObject: progress) {
  try {
    const docRef = doc(db, 'progress', progressObject.student_uid)
    await updateDoc(docRef, {
      games_played: progressObject.games_played,
      points: progressObject.points,
    })
    console.log('Document successfully updated!')
  } catch (err) {
    console.error('Error updating document: ', err)
  }
}

export async function getProgressByStudentUid(studentUid: string) {
  try {
    const progress_collection = collection(db, 'progress')
    const q = query(progress_collection, where('student_uid', '==', studentUid))

    const querySnapshot = await getDocs(q)
    return querySnapshot.docs[0]
  } catch (err) {
    console.error(err)
  }
}
