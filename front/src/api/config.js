import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  xsrfHeaderName: "X-CSRFToken",
  xsrfCookieName: "csrftoken",
  withCredentials: true,
})

export function responseSuccess(response) {
  return response
}

export function responseError(error) {
  return Promise.reject(error)
}

api.interceptors.response.use(responseSuccess, responseError)

export default api