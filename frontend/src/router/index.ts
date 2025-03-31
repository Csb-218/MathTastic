import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminView from '@/views/AdminView.vue'
import AllGames from '@/views/AllGames.vue'
import PlayGame from '@/views/Student/PlayGame.vue'
import AuthenticationForm from '@/views/Authentication/AuthenticationForm.vue'
import EducatorView from '@/views/Educator/EducatorView.vue'
import CreateGame from '@/views/Educator/CreateGame.vue'

import StudentHome from '@/views/Student/StudentHome.vue'
import BalanceScale from '@/views/Student/games/BalanceScale.vue'
import StudentProfile from '@/views/Student/profile/StudentProfile.vue'

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
    },
    {
      path: '/games',
      name: 'games',
      component: AllGames,
    },
    {
      path: '/play/:id',
      name: 'play',
      component: PlayGame,
      meta: { requiresAuth: true, role: 'student' },
    },

    {
      path: '/student',
      name: 'student',
      component: StudentHome,
      meta: { requiresAuth: true, role: 'student' },
      children: [
        {
          path: 'play',
          name: 'balance-scale',
          component: BalanceScale,
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: StudentProfile,
        },
        {
          path: 'progress',
          name: 'progress',
          component: StudentProfile,
        },
        {
          path: 'assessment',
          name: 'assessment',
          component: StudentProfile,
        },
        {
          path: 'workbook',
          name: 'workbook',
          component: StudentProfile,
        }

      ]
    },
    {
      path: '/educator',
      name: 'educator',
      component: EducatorView,
      meta: { requiresAuth: true, role: 'educator' },
      children: [
        {
          path: 'create',
          name: 'create',
          component: CreateGame,
        }
      ]
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
