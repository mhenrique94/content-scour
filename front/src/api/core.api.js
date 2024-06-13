import api from "./config.js"

export default {
  addNewPrompt: async (query) => {
    const formData = new FormData()
    formData.set("query", query)
    const response = await api.post("/api/chatbot/", formData)
    return response.data
  },
  listDocuments: async () => {
    const response = await api.get("/api/document_list/")
    return response.data
  },
  submitDocuments: async (formData) => {
    const response = await api.post("/api/document_upload/", formData)
    return response.data
  },
  deleteDocument: async (id) => {
    const response = await api.delete(`/api/document_delete/${id}/`)
    return response.data
  },
  processDocument: async (id) => {
    const response = await api.post(`/api/document_process/${id}/`)
    return response.data
  },
  ragFromQuery: async (query) => {
    const formData = new FormData()
    formData.set("query", query)
    const response = await api.post(`/api/rag_from_query/`, formData)
    return response.data
  }
}