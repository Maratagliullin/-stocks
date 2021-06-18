const url_backend = process.env.VUE_APP_BACKEND_URL
import {getCookie, comparer} from '@/helpers/utils.js'
export default {
  actions: {
    // Добавление акции возвращает промис с ответом
    add_stock(ctx, data) {
      return new Promise((resolve) => {
        fetch(url_backend + '/api/v1/add_stock/', {
          method: 'POST',
          mode: 'cors',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
        }).then((response) => {
          resolve(response.json())
        })
      })
    },
    // Получение всех акций
    async get_stock(ctx) {
      await fetch(url_backend + '/api/v1/get_stock/')
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          ctx.commit('updateStock', data)
        })
    },
    // Удаление акции смониторинга
    async delete_stock(ctx, id) {
      await fetch(url_backend + '/api/v1/delete_stock/' + id + '/', {
        method: 'DELETE',
        mode: 'cors',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
      }).then(() => {
        ctx.dispatch('get_stock')
      })
    },
  },
  mutations: {
    updateStock(state, stocks) {
      var new_stocks = stocks.filter(comparer(state.stock))

      // changed row
      var class_row = []
      if (state.stock.length == stocks.length && state.stock.length != 0) {
        console.log('changed new value', new_stocks)
        for (var items in new_stocks) {
          var stock_id_changea = new_stocks[items].id
          class_row.push({class: 'info', id: stock_id_changea})
        }
        state.stock_class_row = class_row
      }
      state.stock = stocks
    },
  },
  state: {
    stock: [],
    stock_class_row: [],
  },
  getters: {
    getStocks(state) {
      return state.stock
    },
    getStocksCount(state) {
      return state.stock.length
    },
    stockClassRow(state) {
      return state.stock_class_row
    },
  },
}
