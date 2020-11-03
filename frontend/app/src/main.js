import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VModal from 'vue-js-modal'
import VueResource from 'vue-resource'
import store from './store'

Vue.config.productionTip = false

Vue.use(VModal)
Vue.use(VueResource)

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
