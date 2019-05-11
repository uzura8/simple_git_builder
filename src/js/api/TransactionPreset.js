import client from './client'
import util from '../util';

export default {
  fetch: (params) => {
    const options = { params: params };
    return new Promise((resolve, reject) => {
      client.get('presets', options)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  create: (values) => {
    return new Promise((resolve, reject) => {
      const required_keys = ['name', 'transaction_name', 'amount', 'account_code', 'category_id']
      const params = new URLSearchParams()
      for (let i = 0, n = required_keys.length; i < n; i++) {
        let key = required_keys[i]
        if (values[key] == null) return
        if (!values.hasOwnProperty(key)) return
        params.append(key, values[key]);
      }
      client.post('presets', params)
        .then(res => resolve(res.data))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  update: (presetId, values) => {
    return new Promise((resolve, reject) => {
      const accept_keys = ['name', 'transaction_name', 'amount', 'account_code', 'category_id']
      const params = new URLSearchParams();
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue
        let value = values[key];
        params.append(key, value);
      }
      client.post(`presets/${presetId}`, params)
        .then(res => resolve(res.data))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  delete: (presetId) => {
    return new Promise((resolve, reject) => {
      client.delete(`presets/${presetId}`)
        .then(res => resolve(res.data))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
