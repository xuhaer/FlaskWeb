import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

import blog from './modules/blog'

const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

Vue.use(Vuex)

export default new Vuex.Store({
  // 在非生产环境下，使用严格模式
  strict: process.env.NODE_ENV !== 'production',
  modules: {
    blog: blog
  },
  plugins: [vuexLocal.plugin]
})
