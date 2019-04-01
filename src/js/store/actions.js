import * as types from './mutation-types'
import { Transaction, Category } from '../api'

export default {
  fetchTransactions: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return Transaction.fetch(payload.month)
      .then(({ lists }) => {
        commit(types.FETCH_TRANSACTIONS_LIST, lists)
        commit(types.SET_COMMON_LOADING, false)
      })
      .catch(err => {
        commit(types.SET_COMMON_LOADING, false)
        throw err
      })
  },

  fetchCategories: ({ commit }) => {
    return Category.fetch()
      .then(({ lists }) => {
        commit(types.FETCH_CATEGORIES_LIST, lists)
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

