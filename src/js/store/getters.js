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
}
