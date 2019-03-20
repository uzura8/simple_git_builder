import * as types from './mutation-types'
import { Transaction } from '../api'

export default {
  fetchTransactions: ({ commit }, payload) => {
    return Transaction.fetch(payload.month)
      .then(({ lists }) => {
        commit(types.FETCH_TRANSACTIONS_LIST, lists)
      })
      .catch(err => { throw err })
  },

  //setItemsSortKey: ({ commit }, sortKey) => {
  //  commit(types.SET_ITEM_LIST_SORT_KEY, sortKey)
  //},

  //fetchItemComments: ({ commit }) => {
  //  return Member.fetchItemComments()
  //    .then(({ lists }) => {
  //      commit(types.FETCH_ITEM_COMMENTS, lists)
  //    })
  //    .catch(err => { throw err })
  //},

  //updateItemComment: ({ commit }, payload) => {
  //  return Member.updateItemComment(payload.itemId, payload.comment)
  //    .then(() => {
  //      commit(types.UPDATE_ITEM_COMMENT, payload)
  //    })
  //    .catch(err => { throw err })
  //},
}

