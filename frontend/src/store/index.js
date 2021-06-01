import Vue from 'vue'
import Vuex from 'vuex'
import {add_stock, loading_true,loading_false, remove_stock, get_stock} from './mutation-types.js'
import {Stock} from '../api/stock'

Vue.use(Vuex)




// Состояние
const state = {
  stock: [], // список акций
  loader: false, // loader
}




// Мутации
const mutations = {
  [loading_true](state) {
    state.loader = true
  },
  [loading_false](state) {
    state.loader = false
  },
  // Добавляем тикер в список
  [add_stock](state, stock) {
    if (stock != undefined) {
      state.stock = stock
    }
  },
  // Убираем тикер из списка
  [remove_stock](state, stock) {
      state.stock = stock
  },
  // Задаем список тикеров
  [get_stock](state, {stock}) {
    state.stock = stock
  },
}

// Действия
const actions = {
  createStock({commit}, stockData) {
    commit(loading_true, true)
    Stock.create(stockData).then((stock) => {
      commit(add_stock, stock)
      commit(loading_false, false)
    })
   
  },
  deleteStock({commit}, stock) {
    Stock.delete(stock).then((stock) => {
      commit(remove_stock, stock)
    })
  },
  getStock({commit}) {
    Stock.get_stock().then((stock) => {
      commit(get_stock, {stock})
    })
  },
}

const getters = {

}

export default new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
})
