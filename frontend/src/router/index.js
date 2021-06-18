import Vue from 'vue'
import VueRouter from 'vue-router'
import StockForm from '../components/StockForm.vue'
import Stockpage from '../components/StockPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: '',
    component: StockForm,
  },
  {
    path: '/stockform',
    name: 'stockform',
    component: StockForm,
  },
  {
    path: '/tiker',
    name: 'tiker',
    component: Stockpage,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})

export default router
