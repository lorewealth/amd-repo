export const fmtDate = (iso) =>
  new Date(iso).toLocaleString(
    'ro-RO', { dateStyle: 'medium', timeStyle: 'short'}
  )

export const fmtPct = (n) => `${Number(n).toFixed(2)}%`

export const covClass = (n) =>
  n >= 90 ? 'cov-good' : n >= 70 ? 'cov-warn' : 'cov-bad'
