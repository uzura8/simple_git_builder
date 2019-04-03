import * as types from './mutation-types'
import { util } from '../shared';

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

  [types.UPDATE_TRANSACTION] (state, payload) {
    const transactionId = payload.transactionId
    for (let i = 0, n = state.transaction.list.length; i < n; i++) {
      const transaction = state.transaction.list[i]
      if (transaction.id !== transactionId) continue
      state.transaction.list[i].category_id = payload.categoryId
      break
    }
  },

  [types.FETCH_CATEGORIES_LIST] (state, payload) {
    if (util.isEmpty(payload[0]) || util.isEmpty(payload[0].children)) {
      return []
    }
    state.category.list = payload[0].children
  },
}
