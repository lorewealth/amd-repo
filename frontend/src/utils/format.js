export const fmtDate = (iso) =>
  new Date(iso).toLocaleString(
    'ro-RO', { dateStyle: 'medium', timeStyle: 'short'}
  )

export const fmtPercent = (n) => Number(n).toFixed(2)

export const coverageColor = (n) =>
  n >=90 ? '#3fb950' : n >= 70 ? '#d29922' : '#f85149'

export const covClass = (n) =>
  n >= 90 ? 'cov-good' : n >= 70 ? 'cov-warn' : 'cov-bad'
