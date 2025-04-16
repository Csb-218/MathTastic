import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import EducatorForm from '@/components/blocks/authentication/EducatorForm.vue'
import { createTestingPinia } from '@pinia/testing'

describe('EducatorForm', () => {
  const FormTitleSelector = '[data-test-id=form-title]'
  const FormDescriptionSelector = '[data-test-id=form-description]'
  const EmailInputSelector = '#email'
  const ToggleButtonSelector = '[data-test-id=toggle-form]'
  const PasswordInputSelector = '#password'
  const NameInputSelector = '#name'
  // const ErrorMessageSelector = '[data-test-id=error-message]'

  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    // Create a fresh wrapper for each test with Pinia store
    wrapper = mount(EducatorForm, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              auth: {
                login_user: vi.fn(),
                register_user: vi.fn(),
              },
            },
          }),
        ],
      },
    })
  })

  it('should render properly', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('should display login form by default', () => {
    expect(wrapper.find(FormTitleSelector).text()).toBe('Welcome Back, Educator!')
    expect(wrapper.find(FormDescriptionSelector).text()).toBe('Continue your teaching journey')
    expect(wrapper.find(NameInputSelector).exists()).toBe(false)
  })

  it('should handle email input', async () => {
    const email = 'test@example.com'
    await wrapper.find(EmailInputSelector).setValue(email)
    expect((wrapper.find(EmailInputSelector).element as HTMLInputElement).value).toBe(email)
  })

  it('should handle password input', async () => {
    const password = 'password123'
    await wrapper.find(PasswordInputSelector).setValue(password)
    expect((wrapper.find(PasswordInputSelector).element as HTMLInputElement).value).toBe(password)
  })

  it('should clear form fields when toggling', async () => {
    await wrapper.find(EmailInputSelector).setValue('test@example.com')
    await wrapper.find(PasswordInputSelector).setValue('password123')

    await wrapper.find(ToggleButtonSelector).trigger('click')

    expect((wrapper.find(EmailInputSelector).element as HTMLInputElement).value).toBe('')
    expect((wrapper.find(PasswordInputSelector).element as HTMLInputElement).value).toBe('')
  })
})
