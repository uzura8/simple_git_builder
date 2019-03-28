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
      list = list.filter(transaction =>{
        return transaction.category_id == categoryId
      })
    }
    const keyItems = sortKey.split('-')
    if (keyItems.length === 1) keyItems.push('asc')
    let sort = keyItems[0]
    let order = keyItems[1]
    if (sort === 'date') sort = 'date_int'
    return list.sort(util.compareValues(sort, order))
  },

  singleDimCategories: state => {
    const cates = []
    state.category.list.forEach(function(parentItem) {
      cates.push({
        id: parentItem.id,
        name: parentItem.name,
        pathName: parentItem.name,
      })
      if (!util.isEmpty(parentItem.children)) {
        parentItem.children.forEach(function(item) {
          let pathName = `${parentItem.name} > ${item.name}`
          cates.push({
            id: item.id,
            name: name,
            pathName: pathName,
          })
        })
      }
    })
    return cates
  },

  //getItemCommentByItemId: state => itemId => {
  //  return state.member.itemComments.find(comment => comment.item_id === itemId)
  //},
}
