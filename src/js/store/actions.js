import * as types from './mutation-types'
import { Transaction, Category } from '../api'

export default {
  setHeaderMenuOpen: ({ commit }, isOpen) => {
    commit(types.SET_COMMON_HEADER_MENU_OPEN, isOpen)
  },

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

  updateTransaction: ({ commit }, payload) => {
    return Transaction.update(payload.transactionId, payload.values)
      .then(() => {
        commit(types.UPDATE_TRANSACTION, payload)
      })
      .catch(err => { throw err })
  },
}

