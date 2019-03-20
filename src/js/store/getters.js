//import util from '../util'

export default {
  sortedItems: state => {
    //const keyItems = state.item.listSortKey.split('-')
    //return [...state.item.list].sort(util.compareValues(keyItems[0], keyItems[1]))
    return [...state.transaction.list]
  },

  //getItemCommentByItemId: state => itemId => {
  //  return state.member.itemComments.find(comment => comment.item_id === itemId)
  //},
}
