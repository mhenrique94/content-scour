import api from "./config.js"

export default {
  getCSRF: async () => {
    const response = await api.get("/accounts/get_csrf/")
    return response.data
  },

  getSession: async () => {
    const response = await api.get("/accounts/session/")
    return response.data
  },

  whoAmI: async () => {
    const response = await api.get("/accounts/whoami/")
    return response.data
  },

  login: async(params) => {
    const body = JSON.stringify(params)
    const response = await api.post("/accounts/login/", body)
    return response.data
  },
  
  logout: async() => {
    const response = await api.get("/accounts/logout/")
    return response
  }
}