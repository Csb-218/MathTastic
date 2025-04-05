import { defineStore } from 'pinia'
import type { WeighingObject } from '@/types/game'
import { SoundService } from '@/services/SoundService'

export const useBalanceScaleStore = defineStore('balanceScale', {
  state: () => ({
    objects: [] as WeighingObject[],
    isPlaying: false,
    isFullScreen: false,
    showMessage: false,
    dragInfo: null as {
      obj: WeighingObject
      startX: number
      startY: number
      element: HTMLElement
    } | null,
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
    handleTouchStart(event: TouchEvent, obj: WeighingObject) {
      const element = event.target as HTMLElement
      const touch = event.touches[0]

      event.preventDefault()
      SoundService.play('tap')

      // Store drag info
      this.dragInfo = {
        obj,
        startX: touch.clientX,
        startY: touch.clientY,
        element,
      }

      // Create and style clone
      const clone = element.cloneNode(true) as HTMLElement
      clone.id = 'dragging-clone'
      Object.assign(clone.style, {
        position: 'fixed',
        left: `${touch.clientX - 15}px`, // Center horizontally (30px/2)
        top: `${touch.clientY - 15}px`, // Center vertically (30px/2)
        width: '30px',
        height: '30px',
        zIndex: '9999',
        pointerEvents: 'none',
        opacity: '1',
        transform: 'scale(1.1)',
        boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
        borderRadius: '50%',
        transition: 'none',
      })

      document.body.appendChild(clone)
      element.style.opacity = '0.4' // Make original semi-transparent
    },

    handleTouchMove(event: TouchEvent) {
      if (!this.dragInfo) return
      event.preventDefault()

      const touch = event.touches[0]
      const clone = document.getElementById('dragging-clone')

      if (clone) {
        // Update clone position to follow finger precisely
        clone.style.left = `${touch.clientX - 15}px`
        clone.style.top = `${touch.clientY - 15}px`
      }

      // Update potential drop target highlighting
      const elementUnderTouch = document.elementFromPoint(
        touch.clientX,
        touch.clientY,
      ) as HTMLElement
      const pan = elementUnderTouch?.closest('.pan') as HTMLElement

      document.querySelectorAll('.pan').forEach((p) => {
        const panElement = p as HTMLElement
        panElement.classList.remove('drop-target')
        panElement.style.transform = 'scale(1)'
      })

      if (pan) {
        pan.classList.add('drop-target')
        pan.style.transform = 'scale(1.05)' // Add slight scale effect
      }
    },

    handleTouchEnd(event: TouchEvent) {
      if (!this.dragInfo) return
      event.preventDefault()

      // Reset original element opacity
      this.dragInfo.element.style.opacity = '1'

      const touch = event.changedTouches[0]
      const clone = document.getElementById('dragging-clone')
      clone?.remove()

      // Get drop target
      const elementUnderTouch = document.elementFromPoint(touch.clientX, touch.clientY)
      const pan = elementUnderTouch?.closest('.pan')

      // Handle drop
      if (pan) {
        const panType = pan.classList.contains('left-pan') ? 'left' : 'right'
        this.dragInfo.obj.location = panType
        SoundService.play('drop')
        this.checkWinCondition()
      }

      // Reset pan styles
      document.querySelectorAll('.pan').forEach((p) => {
        const panElement = p as HTMLElement
        panElement.classList.remove('drop-target')
        panElement.style.transform = 'scale(1)'
      })

      this.dragInfo = null
    },

    // Initialize game objects
    initGameObjects(objects: WeighingObject[]) {
      this.objects = [...objects]
    },
  },
})
