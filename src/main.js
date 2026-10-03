import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import HomeView from './views/HomeView.vue'
import CommitmentsView from './views/CommitmentsView.vue'
import GoalsView from './views/GoalsView.vue'
import AnalysisView from './views/AnalysisView.vue'
import GoalTrackingView from './views/GoalTrackingView.vue'
import ReplanningView from './views/ReplanningView.vue'
import HistoryView from './views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/commitments',
      name: 'commitments',
      component: CommitmentsView
    },
    {
      path: '/goals',
      name: 'goals',
      component: GoalsView
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: AnalysisView
    },
    {
      path: '/goal-tracking',
      name: 'goal-tracking',
      component: GoalTrackingView
    },
    {
      path: '/replanning',
      name: 'replanning',
      component: ReplanningView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    }
  ]
})

createApp(App)
  .use(router)
  .mount('#app')