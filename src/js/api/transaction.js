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
  }
}
