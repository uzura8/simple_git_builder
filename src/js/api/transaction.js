import client from './client'

export default {
  fetch: (id=0) => {
    const uri = id ? `transactions/${id}` : 'transactions';
    return new Promise((resolve, reject) => {
      client.get(uri)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  }
}
