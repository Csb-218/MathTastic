import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminView from '@/views/AdminView.vue'
import AllGames from '@/views/AllGames.vue'
import PlayGame from '@/views/Student/PlayGame.vue'
import AuthenticationForm from '@/views/Authentication/AuthenticationForm.vue'
import EducatorView from '@/views/Educator/EducatorHome.vue'
import EducatorDashboard from '@/components/blocks/dashboards/EducatorDashboard.vue'

import StudentHome from '@/views/Student/StudentHome.vue'
import StudentProfile from '@/views/Student/profile/StudentProfile.vue'

// store
import { useAuthStore } from '@/stores/authStore'

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
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true },
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
          path: 'dashboard',
          name: 'student-dashboard',
          component: StudentProfile,
        },
        {
          path: 'progress',
          name: 'student-progress',
          component: StudentProfile,
        },
        {
          path: 'assessment',
          name: 'student-assessment',
          component: StudentProfile,
        },
        {
          path: 'workbook',
          name: 'student-workbook',
          component: StudentProfile,
        },
      ],
    },
    {
      path: '/educator',
      name: 'educator',
      component: EducatorView,
      meta: { requiresAuth: true, role: 'educator' },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: EducatorDashboard,
        },
        {
          path: 'progress',
          name: 'educator-progress',
          component: () => import('@/views/Educator/progress/ProgressSection.vue'),
        },
        {
          path: 'games',
          name: 'educator-games',
          component: () => import('@/views/Educator/games&Activities/GamesGallery.vue'),
        },
        {
          path: 'games/:game_id/create',
          name: 'create-activity',
          component: () => import('@/views/Educator/games&Activities/CreateActivity.vue'),
        },
      ],
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, role: 'admin' },
    },
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
        alert('You do not have permission to access this page.')

        // 3 seconds delay before redirecting to login
        setTimeout(() => {
          next('/login')
        }, 3000)
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
