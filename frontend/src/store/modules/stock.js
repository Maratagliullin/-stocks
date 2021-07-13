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
    async getTickerByIdServer(ctx, payload) {
      return new Promise(function(resolve) {
        fetch(url_backend + '/api/v1/get_stock/' + payload + '/', {
          method: 'GET',
          mode: 'cors',
          headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
          .then((response) => {
            return response.json()
          })
          .then((data) => {
            ctx.commit('updateStock', {data: data, operation: 'getTickerByIdServer'})
            resolve()
          })
      })
    },
    async getTickerDataByServer(ctx, payload) {
      await fetch(url_backend + '/api/v1/get_ticker_data/' + payload + '/', {
        method: 'GET',
        mode: 'cors',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
      })
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          ctx.commit('updateTickerData', data)
        })
    },
    async get_stock(ctx, operation) {
      await fetch(url_backend + '/api/v1/get_stock/')
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          ctx.commit('updateStock', {data: data, operation: operation})
        })
    },
    // Удаление акции смониторинга
    async delete_stock(ctx, payload) {
      await fetch(url_backend + '/api/v1/delete_stock/' + payload.id + '/', {
        method: 'DELETE',
        mode: 'cors',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
      }).then(() => {
        ctx.dispatch('get_stock', payload.operation)
      })
    },
    // Удаление акции смониторинга
    async activate_stock(ctx, payload) {
      await fetch(url_backend + '/api/v1/activate_stock/' + payload.id + '/', {
        method: 'PUT',
        mode: 'cors',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
      }).then(() => {
        ctx.dispatch('get_stock', payload.operation)
      })
    },
  },
  mutations: {
    updateStock(state, payload) {
      var new_stocks = payload.data.filter(comparer(state.stock))

      if (!payload.operation === 'delete' || !payload.operation === 'activate') {
        // changed row
        var class_row = []
        if (state.stock.length == payload.data.length && state.stock.length != 0) {
          for (var items in new_stocks) {
            var stock_id_changea = new_stocks[items].id
            class_row.push({class: 'info', id: stock_id_changea})
          }
          state.stock_class_row = class_row
        }
      }
      state.stock = payload.data
    },
    updateTickerData(state, payload) {
      state.ticker_data = payload
    },
  },
  state: {
    stock: [],
    stock_class_row: [],
    ticker_data: [],
    ticker_name: '',
  },
  getters: {
    getTickerByIdState: (state) => (id) => {
      var ticker = state.stock.find((ticker) => ticker.id === id)
      return ticker
    },
    getTickerNameByState: (state) => (id) => {
      var ticker = state.stock.find((ticker) => ticker.id === id)
      return ticker.stock_ticker
    },
    getTickerNameByServer(state) {
      return state.ticker_name
    },
    getTickerDataJsonInvesting(state) {
      if (state.ticker_data.length != 0) {
        console.log('getTickerDataJsonInvesting', state.ticker_data)
        return JSON.stringify(state.ticker_data.investing.investing_data_json_value)
      }
    },
    getTickerDataJsonTradingview(state) {
      if (state.ticker_data.length != 0) {
        console.log('getTickerDataJsontradingview', state.ticker_data)
        return JSON.stringify(state.ticker_data.tradingview.tradingview_data_json_value)
      }
    },
    getStocks(state) {
      return state.stock
    },
    getTickerData(state) {
      if (state.ticker_data.length != 0) {
      console.log('getTickerData', state.ticker_data)
      return state.ticker_data
    }
    },
    getStocksCount(state) {
      return state.stock.length
    },
    stockClassRow(state) {
      return state.stock_class_row
    },
  },
}
