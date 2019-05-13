import * as types from './mutation-types'
import util from '../util';

export default {
  [types.SET_COMMON_LOADING] (state, isLoading) {
    state.common.isLoading = isLoading
  },

  [types.SET_COMMON_HEADER_MENU_OPEN] (state, isOpen) {
    state.common.isHeaderMenuOpen = isOpen
  },

  [types.FETCH_PERFORMANCE_LIST] (state, payload) {
    state.performance.list = payload
  },

  [types.FETCH_TRANSACTIONS_LIST] (state, payload) {
    state.transaction.list = payload
  },

  [types.CREATE_TRANSACTION] (state, payload) {
    state.transaction.list.push(payload)
  },

  [types.UPDATE_TRANSACTION] (state, payload) {
    const transactionId = payload.transactionId
    const values = payload.values
    const index = state.transaction.list.findIndex(item => item.id === transactionId)
    state.transaction.list.splice(index, 1, values)
  },

  [types.FETCH_TRANSACTION_PRESET_LIST] (state, payload) {
    state.transactionPreset.list = payload
  },

  [types.CREATE_TRANSACTION_PRESET] (state, payload) {
    state.transactionPreset.list.push(payload)
  },

  [types.UPDATE_TRANSACTION_PRESET] (state, payload) {
    const presetId = payload.transactionPresetId
    const values = payload.values
    const index = state.transactionPreset.list.findIndex(item => item.id === presetId)
    state.transaction.list.splice(index, 1, values)
  },

  [types.DELETE_TRANSACTION_PRESET] (state, payload) {
    const presetId = payload.transactionPresetId
    //const values = payload.values
    for (let i = 0, n = state.transactionPreset.list.length; i < n; i++) {
      const transactionPreset = state.transactionPreset.list[i]
      if (transactionPreset.id !== presetId) continue
      state.transactionPreset.list.splice(i, 1)
      break
    }
  },

  [types.FETCH_ACCOUNT_LIST] (state, payload) {
    state.account.list = payload
  },

  [types.FETCH_CATEGORIES_LIST] (state, payload) {
    if (util.isEmpty(payload[0]) || util.isEmpty(payload[0].children)) {
      return []
    }
    state.category.list = payload[0].children
  },

  [types.UPDATE_CATEGORY] (state, payload) {
    for (let i = 0, n = state.category.list.length; i < n; i++) {
      const category = state.category.list[i]
      if (category.id !== payload.category_id) continue

      const accept_keys = ['sublabel']
      for (let key in payload) {
        if (!util.inArray(key, accept_keys)) continue
        if (!payload.hasOwnProperty(key)) continue

        let value = payload[key];
        state.category.list[i][key] = value
      }
      break
    }
  },

  [types.FETCH_BUDGET_LIST] (state, payload) {
    state.budget.list = payload
  },

  [types.UPDATE_BUDGET] (state, payload) {
    for (let i = 0, n = state.budget.list.length; i < n; i++) {
      const budget = state.budget.list[i]
      if (budget.category_id !== payload.category_id) continue

      const accept_keys = ['amount', 'sort_no']
      for (let key in payload) {
        if (!util.inArray(key, accept_keys)) continue
        if (!payload.hasOwnProperty(key)) continue

        let value = payload[key];
        state.budget.list[i][key] = value
      }
      break
    }
  },
}
