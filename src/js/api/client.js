import axios from 'axios'

export default axios.create({
  baseURL: '/api/',
  headers: {
    'ContentType': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  responseType: 'json'
})
