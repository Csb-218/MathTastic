import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthenticationForm from '@/views/Authentication/AuthenticationForm.vue'
import EducatorView from '@/views/Educator/EducatorView.vue'
import StudentView from '@/views/Student/StudentView.vue'
import AdminView from '@/views/AdminView.vue'

// store
import { useAuthStore } from '@/stores/authentication'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: AuthenticationForm,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
    },
    {
      path: '/student',
      name: 'student',
      component: StudentView,
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/educator',
      name: 'educator',
      component: EducatorView,
      meta: { requiresAuth: true, role: 'educator' }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, role: 'admin' }
    }
  ],
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {

  const auth = useAuthStore()

  // Skip auth check for login page
  if (to.path === '/login') {
    next()
    return
  }

  if (to.meta.requiresAuth) {

    if (auth.is_authenticated) {
      // Check role if required
      if (to.meta.role && to.meta.role !== auth.role) {
        next('/login')
      } else {
        next()
      }
    } else {
      next({ path: '/login' })
    }
  } else {
    next()
  }
})

export default router
