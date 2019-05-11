import Vue from 'vue'
import Vuex from 'vuex'
import actions from './actions'
import getters from './getters'
import mutations from './mutations'

Vue.use(Vuex)

const state = {
  common: {
    isLoading: false,
    isHeaderMenuOpen: false,
  },
  performance: {
    list: [],
  },
  transaction: {
    list: [],
  },
  transactionPreset: {
    list: [],
  },
  account: {
    list: [],
  },
  category: {
    list: [],
  },
  budget: {
    list: [],
  },
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  strict: process.env.NODE_ENV !== 'production'
})
