import axios from 'axios'

const api = axios.create({
  // TODO: Deploy -> por em um .env a url
  baseURL: 'http://localhost:8000/api', // base para todas as rotas
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api
