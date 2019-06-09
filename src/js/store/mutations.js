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
    const index = state.transaction.list.findIndex(item => item.id === transactionId)
    state.transaction.list.splice(index, 1, values)
  },

  [types.DELETE_TRANSACTION] (state, payload) {
    const id = payload.transactionId
    for (let i = 0, n = state.transaction.list.length; i < n; i++) {
      const transaction = state.transaction.list[i]
      if (transaction.id !== id) continue
      state.transaction.list.splice(i, 1)
      break
    }
  },
}
