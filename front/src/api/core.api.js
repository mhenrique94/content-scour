import api from "./config.js"

export default {
  addNewPrompt: async (query) => {
    const formData = new FormData()
    formData.set("query", query)
    const response = await api.post("/api/chatbot/", formData)
    return response.data
  },
}