import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import StudentForm from '@/components/blocks/authentication/StudentForm.vue'
import { createTestingPinia } from '@pinia/testing'

describe('StudentForm', () => {
  const FormTitleSelector = '[data-testid=form-title]'
  const FormDescriptionSelector = '[data-testid=form-description]'
  const EmailInputSelector = '#email'
  const PasswordInputSelector = '#password'
  const NameInputSelector = '#name'
  const ErrorMessageSelector = '[data-testid=error-message]'

  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    // Create a fresh wrapper for each test with Pinia store
    wrapper = mount(StudentForm, {
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
    expect(wrapper.find(FormTitleSelector).text()).toBe('Student log in')
    expect(wrapper.find(FormDescriptionSelector).text()).toBe('Welcome back!')
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
})
