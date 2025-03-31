import { defineStore } from 'pinia'
import type { WeighingObject } from '@/types/game'
import { SoundService } from '@/services/SoundService'

export const useBalanceScaleStore = defineStore('balanceScale', {
  state: () => ({
    objects: [] as WeighingObject[],
    isPlaying: false,
    isFullScreen: false,
    showMessage: false,
  }),
  getters: {
    //  pan objects
    availableObjects: (state) => state.objects.filter((obj) => obj.location === 'available'),

    leftPanObjects: (state) => state.objects.filter((obj) => obj.location === 'left'),

    rightPanObjects: (state) => state.objects.filter((obj) => obj.location === 'right'),

    // weight of pan objects
    leftWeight(): number {
      return this.leftPanObjects.reduce((sum, obj) => sum + obj.weight, 0)
    },
    rightWeight(): number {
      return this.rightPanObjects.reduce((sum, obj) => sum + obj.weight, 0)
    },

    // is balanced
    isBalanced(): boolean {
      return this.leftWeight === this.rightWeight
    },
    // has all weights used
    allWeightsUsed() {
      return this.availableObjects.length === 0
    },

    // has won
    hasWon(): boolean {
      return this.isBalanced && this.allWeightsUsed
    },

    // balance status
    balanceStatus(): string {
      return this.hasWon
        ? 'CONGRATULATIONS! YOU WON!'
        : this.isBalanced
          ? 'SCALE IS BALANCED!'
          : 'SCALE IS NOT BALANCED!'
    },

    // tilt angle
    tiltAngle(): number {
      const weightDifference: number = this.rightWeight - this.leftWeight
      return Math.min(Math.max(weightDifference * 5, -30), 30)
    },
  },
  actions: {
    allowDrop(event: DragEvent) {
      event.preventDefault()
    },
    drag(event: DragEvent, obj: WeighingObject) {
      event.dataTransfer?.setData('objId', obj.id)
      SoundService.play('tap')
    },
    checkWinCondition() {
      if (this.hasWon) {
        this.showMessage = true
        SoundService.play('level_up')
      }
    },
    drop(event: DragEvent, pan: 'left' | 'right') {
      event.preventDefault()
      const objId = event.dataTransfer?.getData('objId')
      if (!objId) return

      const obj = this.objects.find((o) => o.id === objId)
      if (obj) {
        obj.location = pan
        SoundService.play('drop')
        this.checkWinCondition()
      }
    },
    resetGame() {
      this.objects.forEach((obj) => {
        obj.location = 'available'
      })
    },
    async startGame(gameContainer: HTMLElement | null) {
      if (!gameContainer) {
        console.error('Game container not found')
        return
      }

      try {
        // Check if fullscreen is supported
        if (document.fullscreenEnabled) {
          // Set playing state first
          this.isPlaying = true
          // Request fullscreen after a small delay to ensure it's tied to user interaction
          await new Promise((resolve) => setTimeout(resolve, 100))
          await gameContainer.requestFullscreen()
          this.isFullScreen = true
        } else {
          console.warn('Fullscreen not supported, starting in windowed mode')
          this.isPlaying = true
        }
      } catch (err) {
        console.error('Failed to enter fullscreen:', err)
        // Fallback to windowed mode
        this.isPlaying = true
      }
    },

    async exitGame() {
      try {
        if (document.fullscreenElement) {
          await document.exitFullscreen()
        }
        this.isPlaying = false
        this.isFullScreen = false
      } catch (err) {
        console.error('Failed to exit fullscreen:', err)
        // Force exit game even if fullscreen fails
        this.isPlaying = false
        this.isFullScreen = false
      }
    },
    fullScreenChange() {
      if (!document.fullscreenElement) {
        this.isPlaying = false
        this.isFullScreen = false
      }
    },
    async toggleFullscreen(gameContainer: HTMLElement | null) {
      if (!document.fullscreenElement) {
        await gameContainer?.requestFullscreen()
        this.isFullScreen = true
      } else {
        await document.exitFullscreen()
        this.isFullScreen = false
      }
    },

    // Initialize game objects
    initGameObjects(objects: WeighingObject[]) {
      this.objects = [...objects]
    },
  },
})
