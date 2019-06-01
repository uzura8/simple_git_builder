import util from '../util'
import { moment } from '../bootstrap';

export default {
  sortedTransactions: state => (categoryId, sortKey) => {

    let list = []
    state.transaction.list.forEach(function(item) {
      item['date_int'] = parseInt(moment(item.date).format('YYYYMMDD'))
      list.push(item)
    })
    if (categoryId) {
      let cateIds = [categoryId]
      const cate = state.category.list.find(item => {
        return item.id === categoryId
      })
      if (cate != null && !util.isEmpty(cate.children)) {
        cate.children.forEach(function(child) {
          cateIds.push(child.id)
        })
      }
      list = list.filter(trans => {
        return util.inArray(trans.category_id, cateIds)
      })
    }
    const keyItems = sortKey.split('-')
    if (keyItems.length === 1) keyItems.push('asc')
    let sort = keyItems[0]
    let order = keyItems[1]
    if (sort === 'date') sort = 'date_int'
    return list.sort(util.compareValues(sort, order))
  },

  transaction: state => (transactionId) => {
    return state.transaction.list.find(item => {
      return item.id === transactionId
    })
  },

  transactionsAmountSum: state => (categoryId = 0) => {
    let sum = 0
    state.transaction.list.forEach(function(item) {
      if (item.is_disabled) return
      if (categoryId && item.category_id !=categoryId) return
      sum += parseInt(item.amount)
    })
    return sum
  },

  transactionPreset: state => (transactionPresetId) => {
    return state.transactionPreset.list.find(item => {
      return item.id === transactionPresetId
    })
  },

  account: state => (accountCode) => {
    return state.account.list.find(item => {
      return item.id === accountCode
    })
  },

  singleDimCategories: state => (isParentOnly = false) => {
    const cates = []
    state.category.list.forEach(function(parentItem) {
      let parentLabel = !util.isEmpty(parentItem.sublabel) ?
        parentItem.sublabel : parentItem.name
      cates.push({
        id: parentItem.id,
        name: parentLabel,
        pathName: parentLabel,
        isParent: true,
      })

      if (isParentOnly) return
      if (util.isEmpty(parentItem.children)) return
      parentItem.children.forEach(function(item) {
        let label = !util.isEmpty(item.sublabel) ? item.sublabel : item.name
        let pathName = `${parentLabel} > ${label}`
        cates.push({
          id: item.id,
          name: item.name,
          pathName: pathName,
          isParent: false,
        })
      })
    })
    return cates
  },

  category: state => (categoryId) => {
    return state.category.list.find(item => {
      return item.id === categoryId
    })
  },

  budgetsAmountTotal: state => {
    let amountTotal = 0
    state.budget.list.forEach(function(item) {
      amountTotal += parseInt(item.amount)
    })
    return amountTotal
  },

  performancesSums: state => () => {
    let sum = 0
    let budget = 0
    state.performance.list.forEach(function(item) {
      sum += parseInt(item.sum)
      budget += parseInt(item.budget)
    })
    return { sum:sum, budget:budget }
  },
}
