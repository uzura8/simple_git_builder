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

  [types.FETCH_CATEGORIES_LIST] (state, payload) {
    if (util.isEmpty(payload[0]) || util.isEmpty(payload[0].children)) {
      return []
    }
    state.category.list = payload[0].children
  },

  //[types.SET_ITEM_LIST_SORT_KEY] (state, value) {
  //  state.item.listSortKey = value
  //},
}
