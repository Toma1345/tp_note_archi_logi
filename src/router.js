import { createRouter, createWebHistory } from 'vue-router'
import QuestionnaireList from './components/QuestionnaireList.vue'
import QuestionnaireDetail from './components/QuestionnaireDetail.vue'
import QuestionnaireForm from './components/QuestionnaireForm.vue'
import QuestionnaireReponse from './components/QuestionnaireReponse.vue'

const routes = [
  { path: '/', redirect: '/questionnaires' },
  { path: '/questionnaires', component: QuestionnaireList },
  { path: '/questionnaire/:id', component: QuestionnaireDetail },
  { path: '/create', component: QuestionnaireForm },
  { path: '/edit/:id', component: QuestionnaireForm },
  { path: '/questionnaire/:id/repondre',  component: QuestionnaireReponse},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
