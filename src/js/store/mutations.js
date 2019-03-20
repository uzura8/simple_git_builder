import * as types from './mutation-types'

export default {
  [types.FETCH_TRANSACTIONS_LIST] (state, payload) {
    state.transaction.list = payload
  },

  //[types.SET_ITEM_LIST_SORT_KEY] (state, value) {
  //  state.item.listSortKey = value
  //},
}
