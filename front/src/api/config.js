import axios from "axios"

const cookie_csrf = document.cookie.match('(^|;)\\s*' + "csrftoken" + '\\s*=\\s*([^;]+)')?.pop() || ''

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  // xsrfHeaderName: "X-CSRFToken",
  // xsrfCookieName: "csrftoken",
  withCredentials: true,
  headers: {
    "X-CSRFToken": cookie_csrf
  }
})

export default api