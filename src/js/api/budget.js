import client from './client'
import util from '../util';

export default {
  fetch: (params) => {
    const uri = 'budgets';
    const options = { params: params };
    return new Promise((resolve, reject) => {
      client.get(uri, options)
        .then(res => resolve({ lists: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },

  update: (categoryId, values) => {
    return new Promise((resolve, reject) => {
      const accept_keys = ['amount', 'sort_no']
      const params = new URLSearchParams();
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue
        let value = values[key];
        params.append(key, value);
      }
      client.post(`budgets/${categoryId}`, params)
        .then(res => resolve({ item: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
