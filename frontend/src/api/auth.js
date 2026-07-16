import client, { API_BASE } from './client'

export function loginUrl(redirectUri) {
  return `${API_BASE}/auth/login?redirect_uri=` + encodeURIComponent(redirectUri)
}

export async function exchangeCode(code) {
  const form = new URLSearchParams()
  form.append('code', code)
  return client.post('/auth/token', form).then((r) => r.data)
}
