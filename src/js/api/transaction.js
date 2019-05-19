import client from './client'
import util from '../util';

export default {
  fetch: (params) => {
    const uri = 'transactions';
    const options = { params: params };
    return new Promise((resolve, reject) => {
      client.get(uri, options)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  create: (values) => {
    return new Promise((resolve, reject) => {
      const required_keys = ['name', 'amount', 'date', 'category_id', 'account_code']
      const params = new URLSearchParams()
      for (let i = 0, n = required_keys.length; i < n; i++) {
        let key = required_keys[i]
        if (values[key] === null) throw new Error(`No value '${key}'`);
        if (!values.hasOwnProperty(key)) throw new Error(`No value '${key}'`);
        params.append(key, values[key]);
      }
      client.post('transactions', params)
        .then(res => resolve(res.data))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  update: (transactionId, values) => {
    return new Promise((resolve, reject) => {
      const accept_keys = ['name', 'amount', 'date', 'category_id', 'account_code', 'is_disabled']
      const params = new URLSearchParams();
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue
        let value = values[key];
        params.append(key, value);
      }
      client.post(`transactions/${transactionId}`, params)
        .then(res => resolve(res.data))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
