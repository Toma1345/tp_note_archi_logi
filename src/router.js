import { createRouter, createWebHistory } from 'vue-router'
import QuestionnaireList from './components/QuestionnaireList.vue'
import QuestionnaireDetail from './components/QuestionnaireDetail.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: QuestionnaireList,
  },
  {
    path: '/questionnaires/:id',
    name: 'questionnaire-details',
    component: QuestionnaireDetail,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
