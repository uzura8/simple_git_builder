import * as types from './mutation-types'
import util from '../util';

export default {
  [types.SET_COMMON_LOADING] (state, isLoading) {
    state.common.isLoading = isLoading
  },

  [types.SET_COMMON_HEADER_MENU_OPEN] (state, isOpen) {
    state.common.isHeaderMenuOpen = isOpen
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
    for (let i = 0, n = state.transaction.list.length; i < n; i++) {
      const transaction = state.transaction.list[i]
      if (transaction.id !== transactionId) continue

      const accept_keys = ['name', 'amount', 'date', 'category_id', 'is_disabled']
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue

        let value = values[key];
        state.transaction.list[i][key] = value
      }
      break
    }
  },

  [types.FETCH_CATEGORIES_LIST] (state, payload) {
    if (util.isEmpty(payload[0]) || util.isEmpty(payload[0].children)) {
      return []
    }
    state.category.list = payload[0].children
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
