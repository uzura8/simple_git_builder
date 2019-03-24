import util from '../util'

export default {
  sortedTransactions: state => categoryId => {
    if (categoryId) {
      return [...state.transaction.list].filter(transaction =>{
        return transaction.category_id == categoryId
      })
    }
    return [...state.transaction.list]
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
