import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import AuthForm from '../blocks/authentication/AuthForm.vue'
import { useAuthPageStore } from '@/stores/Authentication/authPageStore'
import { useAuth } from '@/composables/auth'

const handleSubmitSpy = vi.fn()
const handleGoogleSpy = vi.fn()
const clearErrorSpy = vi.fn()

// Mock the auth composable
vi.mock('@/composables/auth', () => ({
  useAuth: () => ({
    handleSubmit: handleSubmitSpy,
    handleGoogle: handleGoogleSpy,
    errorMessage: '',
    clearError: clearErrorSpy,
  }),
}))

describe('AuthForm', () => {
  const selectors = {
    formTitle: '[data-test-id="form-title"]',
    formDescription: '[data-test-id="form-description"]',
    toggleButton: '[data-test-id="toggle-form"]',
    nameInput: 'input[id="name"]',
    emailInput: 'input[type="email"]',
    passwordInput: 'input[type="password"]',
    submitButton: 'button[type="submit"]',
    googleButton: 'button[type="button"]',
    form: 'form',
    errorMessage: '[data-test-id="error-message"]',
  }

  beforeEach(() => {
    setActivePinia(createPinia())
    handleSubmitSpy.mockClear()
    handleGoogleSpy.mockClear()
  })

  it('renders login form for students by default', () => {
    const wrapper = mount(AuthForm)
    expect(wrapper.find(selectors.formTitle).text()).toContain('Student log in')
    expect(wrapper.find(selectors.formDescription).text()).toContain('Welcome back!')
  })

  it('toggles between login and signup forms', async () => {
    const wrapper = mount(AuthForm)

    // Check initial login state
    expect(wrapper.find(selectors.formTitle).text()).toContain('Student log in')
    expect(wrapper.find(selectors.nameInput).exists()).toBe(false)

    // Toggle to signup
    await wrapper.find(selectors.toggleButton).trigger('click')

    // Verify signup state
    expect(wrapper.find(selectors.formTitle).text()).toContain('Sign up to play!')
    expect(wrapper.find(selectors.nameInput).exists()).toBe(true)
  })

  it('submits login form with correct data', async () => {
    const wrapper = mount(AuthForm)

    await wrapper.find(selectors.emailInput).setValue('test@example.com')
    await wrapper.find(selectors.passwordInput).setValue('password123')
    await wrapper.find(selectors.form).trigger('submit')

    expect(handleSubmitSpy).toHaveBeenCalledWith('test@example.com', 'password123', '')
  })

  it('submits signup form with correct data', async () => {
    const wrapper = mount(AuthForm)
    const auth = useAuth()
    const authStore = useAuthPageStore()

    // Switch to signup mode
    await wrapper.find(selectors.toggleButton).trigger('click')
    authStore.setStudent(false)
    await wrapper.vm.$nextTick()

    await wrapper.find(selectors.nameInput).setValue('John Doe')
    await wrapper.find(selectors.emailInput).setValue('test@example.com')
    await wrapper.find(selectors.passwordInput).setValue('password123')
    await wrapper.find(selectors.form).trigger('submit')

    expect(auth.handleSubmit).toHaveBeenCalledWith('test@example.com', 'password123', 'John Doe')
  })

  it('handles Google authentication', async () => {
    const wrapper = mount(AuthForm)

    await wrapper.find(selectors.googleButton).trigger('click')
    expect(handleGoogleSpy).toHaveBeenCalled()
  })

  it('switches between student and educator views', async () => {
    const wrapper = mount(AuthForm)
    const authStore = useAuthPageStore()

    // Check initial student view
    expect(wrapper.find(selectors.formTitle).text()).toContain('Student log in')

    // Switch to educator view
    authStore.setStudent(false)
    await wrapper.vm.$nextTick()

    expect(wrapper.find(selectors.formTitle).text()).toContain('Welcome Back, Educator')
  })

  it('disables submit button during loading states', async () => {
    const wrapper = mount(AuthForm)
    const authStore = useAuthPageStore()

    // Check initial state
    expect(wrapper.find(selectors.submitButton).attributes('disabled')).toBeUndefined()

    // Set loading state
    authStore.emailLoading = true
    await wrapper.vm.$nextTick()

    expect(wrapper.find(selectors.submitButton).attributes('disabled')).toBeDefined()
  })

  it('clears error message on input focus', async () => {
    const wrapper = mount(AuthForm)

    await wrapper.find(selectors.emailInput).trigger('focus')
    expect(clearErrorSpy).toHaveBeenCalled()
  })
})
