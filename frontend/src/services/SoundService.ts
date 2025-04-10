import { drop, game_complete, level_up, tap } from '@/assets/sound_effects'

export class SoundService {
  private static sounds: { [key: string]: HTMLAudioElement } = {
    drop: new Audio(drop),
    win: new Audio(game_complete),
    level_up: new Audio(level_up),
    tap: new Audio(tap),
  }

  static play(soundName: keyof typeof SoundService.sounds): void {
    const sound = this.sounds[soundName]
    if (sound) {
      sound.currentTime = 0 // Reset sound to start
      sound.play().catch((err) => console.error('Error playing sound:', err))
    }
  }
}
