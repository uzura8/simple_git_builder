import client from './client'

export default {
  fetch: (params) => {
    const uri = 'performance';
    const options = { params: params };
    return new Promise((resolve, reject) => {
      client.get(uri, options)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
