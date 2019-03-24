import util from '../util'

export default {
  sortedTransactions: state => (categoryId, sortKey) => {
    let list = [...state.transaction.list]
    if (categoryId) {
      list = list.filter(transaction =>{
        return transaction.category_id == categoryId
      })
    }
    const keyItems = sortKey.split('-')
    if (keyItems.length === 1) keyItems.push('asc')
    return list.sort(util.compareValues(keyItems[0], keyItems[1]))
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
