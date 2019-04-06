import client from './client'
import util from '../util';

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

  update: (transactionId, values) => {
    return new Promise((resolve, reject) => {
      const accept_keys = ['category_id', 'is_disabled']
      const params = new URLSearchParams();
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue
        let value = values[key];
        params.append(key, value);
      }
      client.post(`transactions/${transactionId}`, params)
        .then(() => resolve())
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
