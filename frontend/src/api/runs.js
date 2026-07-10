import api from './client'

export function getRuns()
{
  return api.get('/runs')
}

export function getRun(id)
{
  return api.get(`/runs/${id}`)
}
