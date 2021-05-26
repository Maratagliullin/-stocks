import Vue from 'vue'
import App from './App.vue'
import {BootstrapVue, BVToastPlugin, IconsPlugin} from 'bootstrap-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueRouter from 'vue-router'
import Vuex from 'vuex'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import '../src/assets/styles/style.css'
import router from './router'
import store from './store'

Vue.use(Vuex)

//vue Router
Vue.use(VueRouter)
Vue.use(BootstrapVue)
//Axios-vue
Vue.use(VueAxios, axios)

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
Vue.use(BVToastPlugin)

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  beforeMount: function() {
    this.$store.dispatch('getStock')
  },
  render: (h) => h(App),
}).$mount('#app')
