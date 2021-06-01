import Vue from 'vue'
import Vuex from 'vuex'
import stock from './modules/stock'

Vue.use(Vuex)
export default new Vuex.Store({
    actions:{},
    mutations:{},
    state:{},
    getters:{},
    modules:{
        stock
    }
})