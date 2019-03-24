export default {
  isEmpty: (data) => {
    if (data === null) return true;
    if (data === undefined) return true;
    if (data === false) return true;
    if (data === '') return true;
    if (data === '0') return true;
    if (data === 0) return true;
    if (typeof data === 'object') {
      if (Array.isArray(data)) return data.length === 0;
      if (Object.keys(data).length > 0) return false;
      if (
        typeof Object.getOwnPropertySymbols !== 'undefined' &&
        Object.getOwnPropertySymbols(data).length > 0
      )
        return false;
      if (data.valueOf().length !== undefined)
        return data.valueOf().length === 0;
      if (typeof data.valueOf() !== 'object') return this.isEmpty(data.valueOf());
    }
    return false;
  },

  inArray: (value, array) => {
    return [].indexOf.call(array, value) > -1;
  },

  compareValues: (key, order='asc') => {
    return function(a, b) {
      if (a.hasOwnProperty(key) && b.hasOwnProperty(key)) {
        const varA = (typeof a[key] === 'string') ?
          a[key].toUpperCase() : a[key]
        const varB = (typeof b[key] === 'string') ?
          b[key].toUpperCase() : b[key]

        let comparison = 0;
        if (varA > varB) {
          comparison = 1
        } else if (varA < varB) {
          comparison = -1
        }
        return (
          (order == 'desc') ? (comparison * -1) : comparison
        )
      } else {
        if (!a.hasOwnProperty(key)) return -1
        if (!b.hasOwnProperty(key)) return -1
      }
      return 0
    }
  },

  substr: (text, len, truncation='') => {
    const text_array = text.split('')
    let count = 0
    let str = ''
    for (let i = 0, m = text_array.length; i < m; i++) {
      let n = escape(text_array[i])
      if (n.length < 4) {
        count++
      } else {
        count += 2;
      }
      if (count > len) {
        return str + truncation
      }
      str += text.charAt(i)
    }
    return text
  },
}
