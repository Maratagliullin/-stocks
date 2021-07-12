import Vue from 'vue'
import VueRouter from 'vue-router'
import StockForm from '../components/StockForm.vue'
import Stockpage from '../components/StockPage.vue'
import TickerPage from '../components/TickerPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: '',
    component: StockForm,
  },
  {
    path: '/stockform',
    name: 'StockForm',
    component: StockForm,
  },
  {
    path: '/ticker',
    name: 'StockPage',
    component: Stockpage,
  },
  {
    path: '/ticker/:id',
    name: 'TickerPage',
    component: TickerPage,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
})

export default router
