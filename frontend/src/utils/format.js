export const fmtDate = (iso) =>
  new Date(iso).toLocaleString(
    'ro-RO', { dateStyle: 'medium', timeStyle: 'short'}
  )

export const fmtPercent = (n) => Number(n).toFixed(2)

export const coverageColor = (n) =>
  n >= 95 ? '#3fb950' : n >= 80 ? '#d29922' : '#f85149'

export const covClass = (n) =>
  n >= 95 ? 'cov-good' : n >= 80 ? 'cov-warn' : 'cov-bad'

export const covStatus = (n) =>
  Number(n) >= 95 ? 'PASSED' : 'FAILED'

export const covBadgeClass = (n) =>
  Number(n) >= 95 ? 'badge-good' : Number(n) >= 80 ? 'badge-warn' : 'badge-bad'
