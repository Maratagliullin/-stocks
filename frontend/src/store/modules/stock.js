export default {
  actions: {
    // Добавление акции возвращает промис с ответом
    add_stock(ctx, data) {
      return new Promise((resolve) => {
        fetch('http://localhost:8000/api/v1/add_stock/', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
          },
        }).then((response) => {
          resolve(response.json())
        })
      })
    },
    // Получение всех акций
    async get_stock(ctx) {
      await fetch('http://localhost:8000/api/v1/get_stock/')
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          ctx.commit('updateStock', data)
        })
    },
    // Удаление акции смониторинга
    async delete_stock(ctx, id) {
      await fetch('http://localhost:8000/api/v1/delete_stock/' + id + '/', {method: 'DELETE'}).then(() => {
        ctx.dispatch('get_stock')
      })
    },
  },
  mutations: {
    updateStock(state, stocks) {
      state.stock = stocks
    },
  },
  state: {
    stock: [],
  },
  getters: {
    getStocks(state) {
      return state.stock
    },
    getStocksCount(state) {
      return state.stock.length
    },
  },
}
