import api from './client'

export function getRuns()
{
  return api.get('/runs/')
}

export function getRun(id)
{
  return api.get(`/runs/${id}`)
}

export async function uploadRun(file) {
  const form = new FormData()
  form.append('file', file)
  return api.post('/runs/upload', form, {
    headers: {'Content-Type':'multipart/form-data'},
  }).then((r) => r.data)
}
