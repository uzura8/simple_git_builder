import client from './client'
import util from '../util';

export default {
  fetch: () => {
    const uri = 'categories';
    const options = {};
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
      const accept_keys = ['sublabel', 'is_monthly']
      const params = new URLSearchParams();
      for (let key in values) {
        if (!util.inArray(key, accept_keys)) continue
        if (!values.hasOwnProperty(key)) continue
        let value = values[key];
        params.append(key, value);
      }
      client.post(`categories/${categoryId}`, params)
        .then(res => resolve({ item: res.data }))
        .catch(err => {
          reject(new Error(err.response.data.message || err.message))
        })
    })
  },
}
