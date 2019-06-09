import * as types from './mutation-types'
import { Performance, Transaction, TransactionPreset, Account, Category, Budget } from '../api'

export default {
  setHeaderMenuOpen: ({ commit }, isOpen) => {
    commit(types.SET_COMMON_HEADER_MENU_OPEN, isOpen)
  },

  setIsLoading: ({ commit }, isLoading) => {
    commit(types.SET_COMMON_LOADING, isLoading)
  },

  fetchTransactions: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return Transaction.fetch(payload)
      .then(({ lists }) => {
        commit(types.FETCH_TRANSACTIONS_LIST, lists)
        commit(types.SET_COMMON_LOADING, false)
      })
      .catch(err => {
        commit(types.SET_COMMON_LOADING, false)
        throw err
      })
  },

  createTransaction: ({ commit }, payload) => {
    return Transaction.create(payload)
      .then((item) => {
        commit(types.CREATE_TRANSACTION, item)
      })
      .catch(err => { throw err })
  },

  updateTransaction: ({ commit }, payload) => {
    return Transaction.update(payload.transactionId, payload.values)
      .then((item) => {
        commit(types.UPDATE_TRANSACTION, {
          transactionId: payload.transactionId,
          values: item,
        })
      })
      .catch(err => { throw err })
  },

  deleteTransaction: ({ commit }, presetId) => {
    return Transaction.delete(presetId)
      .then((item) => {
        const data = {
          transactionId: presetId,
          values: item,
        }
        commit(types.DELETE_TRANSACTION, data)
      })
      .catch(err => { throw err })
  },
}

