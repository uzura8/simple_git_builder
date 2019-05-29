import * as types from './mutation-types'
import { Performance, Transaction, TransactionPreset, Account, Category, Budget } from '../api'

export default {
  setHeaderMenuOpen: ({ commit }, isOpen) => {
    commit(types.SET_COMMON_HEADER_MENU_OPEN, isOpen)
  },

  fetchPerformances: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return Performance.fetch(payload)
      .then(({ lists }) => {
        commit(types.FETCH_PERFORMANCE_LIST, lists)
        commit(types.SET_COMMON_LOADING, false)
      })
      .catch(err => {
        commit(types.SET_COMMON_LOADING, false)
        throw err
      })
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

  fetchTransactionPresets: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return TransactionPreset.fetch(payload)
      .then(({ lists }) => {
        commit(types.FETCH_TRANSACTION_PRESET_LIST, lists)
        commit(types.SET_COMMON_LOADING, false)
      })
      .catch(err => {
        commit(types.SET_COMMON_LOADING, false)
        throw err
      })
  },

  createTransactionPreset: ({ commit }, payload) => {
    return TransactionPreset.create(payload)
      .then((item) => {
        commit(types.CREATE_TRANSACTION_PRESET, item)
      })
      .catch(err => { throw err })
  },

  updateTransactionPreset: ({ commit }, payload) => {
    return TransactionPreset.update(payload.transactionPresetId, payload.values)
      .then((item) => {
        const data = {
          transactionPresetId: payload.transactionPresetId,
          values: item,
        }
        commit(types.UPDATE_TRANSACTION_PRESET, data)
      })
      .catch(err => { throw err })
  },

  deleteTransactionPreset: ({ commit }, presetId) => {
    return TransactionPreset.delete(presetId)
      .then((item) => {
        const data = {
          transactionPresetId: presetId,
          values: item,
        }
        commit(types.DELETE_TRANSACTION_PRESET, data)
      })
      .catch(err => { throw err })
  },

  fetchAccounts: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return Account.fetch(payload)
      .then(({ lists }) => {
        commit(types.FETCH_ACCOUNT_LIST, lists)
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

  updateCategory: ({ commit }, payload) => {
    return Category.update(payload.categoryId, payload.values)
      .then(({item}) => {
        commit(types.UPDATE_CATEGORY, item)
      })
      .catch(err => { throw err })
  },

  fetchBudgets: ({ commit }, payload) => {
    commit(types.SET_COMMON_LOADING, true)
    return Budget.fetch(payload)
      .then(({ lists }) => {
        commit(types.FETCH_BUDGET_LIST, lists)
        commit(types.SET_COMMON_LOADING, false)
      })
      .catch(err => {
        commit(types.SET_COMMON_LOADING, false)
        throw err
      })
  },

  updateBudget: ({ commit }, payload) => {
    return Budget.update(payload.categoryId, payload.values)
      .then(({item}) => {
        commit(types.UPDATE_BUDGET, item)
      })
      .catch(err => { throw err })
  },
}

