import api from "./config.js"

export default {
  addNewPrompt: async (query) => {
    const json = JSON.stringify({ query })
    const response = await api.post(
      "/api",
      json
    )
    return response.data
  },
}