import client from './client'

export default {
  fetch: (month) => {
    const uri = 'transactions';
    const options = { params: { month: month } };
    return new Promise((resolve, reject) => {
      client.get(uri, options)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  updateCategoryId: (transactionId, categoryId) => {
    return new Promise((resolve, reject) => {
      const params = new URLSearchParams();
      params.append('category_id', categoryId);
      client.post(`transactions/${transactionId}`, params)
        .then(() => resolve())
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
